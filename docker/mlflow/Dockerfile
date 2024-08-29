# Use a slim Python base image
FROM python:3.10.14-slim

# Install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    mlflow[extras] \
    psycopg2-binary \
    boto3 \
    cryptography \
    pymysql

# Create a directory for the startup script
WORKDIR /app

# Copy the startup script into the container
COPY mlflow-start.sh /app/mlflow-start.sh

# Ensure the startup script is executable
RUN chmod +x /app/mlflow-start.sh

# Set the entrypoint to the startup script
ENTRYPOINT ["/bin/bash", "/app/mlflow-start.sh"]
