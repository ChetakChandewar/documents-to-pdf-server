# Use a lightweight Debian image
FROM debian:latest

# Install dependencies and LibreOffice
RUN apt-get update && \
    apt-get install -y libreoffice libreoffice-writer python3 python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Set the working directory
WORKDIR /app

# Copy required files
COPY requirements.txt .
COPY server.py .

# Expose port 8080
EXPOSE 8080

# Run the server
CMD ["python3", "server.py"]
