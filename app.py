import os
import uuid
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_file  # Import send_file

# Initialize Flask app
app = Flask(__name__)

# Constants for folder locations
INPUT_FOLDER = 'images'
OUTPUT_FOLDER = 'outputs'

# To store circular objects by image_id
circular_objects = {}

# Ensure output folder exists
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def process_image(image_path, image_filename):
    """
    Processes an image to detect circular objects using HoughCircles, returns valid circles.
    :param image_path: Path of the image
    :param image_filename: The name of the image
    :return: List of valid circles (x, y, radius)
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Gaussian blur to reduce noise and improve detection
    blurred_image = cv2.GaussianBlur(image, (15, 15), 0)

    # Detect circles using HoughCircles
    circles = cv2.HoughCircles(blurred_image, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30, param1=50, param2=30, minRadius=10, maxRadius=100)

    if circles is not None:
        # Convert the (x, y, radius) to integer
        circles = np.round(circles[0, :]).astype("int")
        valid_circles = []

        for (x, y, radius) in circles:
            # Filter out small and unreasonably large circles
            if 10 < radius < 100:  # You can adjust the radius range
                valid_circles.append((x, y, radius))

        return valid_circles
    return []  # Return empty list if no circles are found

def convert_to_native_int(obj):
    """Convert NumPy int64 to native int recursively for JSON serialization."""
    if isinstance(obj, dict):
        return {key: convert_to_native_int(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_native_int(item) for item in obj]
    elif isinstance(obj, np.int64):  # Handle NumPy int64 specifically
        return int(obj)  # Convert to native Python int
    return obj

@app.route('/')
def home():
    return 'Welcome to the Coin Challenge API!'

@app.route('/upload', methods=['POST'])
def upload_image():
    """
    Upload an image, process it to detect circles, and return the result.
    :return: JSON response with image ID and result message
    """
    file = request.files['image']
    if not file:
        return jsonify({"error": "No file provided"}), 400

    # Generate a unique image ID
    image_id = str(uuid.uuid4())
    image_filename = file.filename
    image_path = os.path.join(INPUT_FOLDER, image_filename)

    # Save the uploaded image to the input folder
    file.save(image_path)

    # Process the image to detect circles
    valid_circles = process_image(image_path, image_filename)

    # Store the detected circles in the global circular_objects dictionary
    circular_objects[image_id] = []

    for (x, y, radius) in valid_circles:
        circular_objects[image_id].append({
            "id": str(uuid.uuid4()),  # Unique reference for each circle
            "bounding_box": [x - radius, y - radius, x + radius, y + radius],
            "centroid": [x, y],
            "radius": radius
        })

    # Save the processed image
    output_image_path = os.path.join(OUTPUT_FOLDER, f"processed_{image_filename}")
    image = cv2.imread(image_path)
    for (x, y, radius) in valid_circles:
        cv2.circle(image, (x, y), radius, (0, 255, 0), 4)  # Draw circles on the image
    cv2.imwrite(output_image_path, image)

    return jsonify({
        "image_id": image_id,
        "message": "Image uploaded and processed successfully"
    })

@app.route('/circles/<image_id>', methods=['GET'])
def get_circles(image_id):
    """
    Get the details of circles detected in an image.
    :param image_id: Unique ID for the uploaded image
    :return: JSON response with circle details
    """
    if image_id not in circular_objects:
        return jsonify({"error": "Image ID not found"}), 404

    # Convert any NumPy int64 values to native int types
    circle_data = convert_to_native_int(circular_objects[image_id])

    return jsonify(circle_data), 200

@app.route('/processed_image/<image_filename>', methods=['GET'])
def get_processed_image(image_filename):
    """
    Retrieve the processed image with detected circles overlaid.
    :param image_filename: Name of the processed image file
    :return: Processed image as a response
    """
    image_path = os.path.join(OUTPUT_FOLDER, image_filename)
    if not os.path.exists(image_path):
        return jsonify({"error": "Processed image not found"}), 404

    return send_file(image_path, mimetype='image/png')  # This sends the image file

if __name__ == '__main__':
    app.run(debug=True)
