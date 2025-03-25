# Use Ubuntu as the base image
FROM ubuntu:latest

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update system and install dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    python3 \
    python3-pip \
    && apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the server script
COPY server.py .

# Create necessary directories
RUN mkdir -p /app/uploads /app/output

# Expose the port for Flask
EXPOSE 8080

# Start the Flask server
CMD ["python3", "server.py"]
