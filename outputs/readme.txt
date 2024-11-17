CoinChallenge App
=================

CoinChallenge is a Flask-based application for uploading coin images, segmenting circular objects, and processing them for further analysis. This application provides endpoints to upload images and retrieve information about the segmented objects.

Features:
---------
- **Upload Coin Images**: Users can upload coin images via a POST request.
- **Get Object Info**: After processing, users can retrieve information about the circular objects found in the image.
- **Dockerized Application**: This app is fully containerized with Docker for easy deployment and scalability.

Prerequisites:
--------------
To run this application locally, you need to have the following installed:
- Docker (https://www.docker.com/get-started)
- Python (https://www.python.org/downloads/) (if running without Docker)
- Flask and required Python dependencies (if running locally)

Installation and Setup:
------------------------
1. Clone the repository (if applicable):
   git clone https://github.com/yourusername/CoinChallenge.git
   cd CoinChallenge

2. Build the Docker image:
   docker build -t coin-challenge-app .

3. Run the application:
   docker run -d -p 5000:5000 coin-challenge-app

This will start the app on port 5000. You can access it via http://localhost:5000 on your local machine.

API Endpoints:
--------------
1. **Upload Image** (POST request)
   URL: http://localhost:5000/upload
   Method: POST
   Content-Type: multipart/form-data
   Request Body:
     - file: The coin image to be uploaded.
   Response:
     - 200 OK if the image is successfully uploaded and processed.
     - Returns details of the segmented circular objects found in the image (JSON format).

   Example:
   curl -X POST -F "file=@path_to_your_image.jpg" http://localhost:5000/upload

2. **Get Object Info** (GET request)
   URL: http://localhost:5000/info
   Method: GET
   Response:
     - JSON object containing the information about the segmented circular objects in the uploaded image.

Usage Example:
--------------
1. Uploading an image of a coin:
   curl -X POST -F "file=@coin_image.jpg" http://localhost:5000/upload

2. Get information about the objects found:
   curl http://localhost:5000/info

Docker Support:
---------------
This application is containerized using Docker, which allows for easy deployment. The Dockerfile has been configured to install all necessary dependencies and run the Flask app.

To build and run the Docker container:

- **Build the image**:
  docker build -t coin-challenge-app .

- **Run the container**:
  docker run -d -p 5000:5000 coin-challenge-app

Contributing:
-------------
If you want to contribute to this project:
1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes and commit them (git commit -m 'Add new feature').
4. Push to the branch (git push origin feature-branch).
5. Open a Pull Request with a description of your changes.

License:
--------
This project is licensed under the MIT License - see the LICENSE.md file for details.
