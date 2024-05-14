# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Set a default port number
ENV DASH_PORT=9069

# Make the port defined in DASH_PORT available to the world outside this container
EXPOSE $DASH_PORT

# Run the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:9069", "main:app"]
