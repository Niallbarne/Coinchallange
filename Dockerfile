# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory to /app inside the container
WORKDIR /app

# Copy the entire project directory contents into the container at /app
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to be able to access the app from outside the container
EXPOSE 5000

# Set an environment variable to specify the Flask app entry point
ENV FLASK_APP=app.py

# Run the Flask app when the container starts
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
