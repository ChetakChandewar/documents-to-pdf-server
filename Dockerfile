# Use a stable Ubuntu base image
FROM ubuntu:22.04

# Set non-interactive mode to avoid installation prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update system and install dependencies
RUN apt-get update && \
    apt-get install -y libreoffice python3 python3-pip && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the server script
COPY server.py .

# Create necessary directories
RUN mkdir -p /app/uploads /app/output

# Expose Flask API port
EXPOSE 8080

# Start the Flask server
CMD ["python3", "server.py"]
