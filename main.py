import os
import uuid
import cv2
from app import process_image, circular_objects, INPUT_FOLDER, OUTPUT_FOLDER

# Ensure output folder exists
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def process_and_save_image(image_filename):
    """
    This function loads an image, processes it for circular object detection, and stores the results.
    It then saves the processed image into the output folder and stores the circle details in the global circular_objects dictionary.
    """
    # Path of the image
    image_path = os.path.join(INPUT_FOLDER, image_filename)

    # Process the image and detect circles
    valid_circles = process_image(image_path, image_filename)

    # Generate a unique image ID
    image_id = str(uuid.uuid4())
    circular_objects[image_id] = []

    for (x, y, radius) in valid_circles:
        circular_objects[image_id].append({
            "id": str(uuid.uuid4()),  # Unique reference for each circle
            "bounding_box": (x - radius, y - radius, x + radius, y + radius),
            "centroid": (x, y),
            "radius": radius
        })

    # Save the processed image
    output_image_path = os.path.join(OUTPUT_FOLDER, f"processed_{image_filename}")
    image = cv2.imread(image_path)
    for (x, y, radius) in valid_circles:
        cv2.circle(image, (x, y), radius, (0, 255, 0), 4)  # Draw circles on the image
    cv2.imwrite(output_image_path, image)
    print(f"Processed image saved at: {output_image_path}")
    print(f"Detected circles for image {image_filename}: {circular_objects[image_id]}")

if __name__ == "__main__":
    image_filename = "example_image.png"
    process_and_save_image(image_filename)
