#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Ensure MinIO credentials are set in the environment
export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
export MLFLOW_S3_ENDPOINT_URL=${MLFLOW_S3_ENDPOINT_URL}

# Print environment variables for debugging purposes
echo "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}"
echo "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}"
echo "MLFLOW_S3_ENDPOINT_URL=${MLFLOW_S3_ENDPOINT_URL}"

# Write AWS credentials to file
mkdir -p ~/.aws
cat <<EOF > ~/.aws/credentials
[default]
aws_access_key_id=${AWS_ACCESS_KEY_ID}
aws_secret_access_key=${AWS_SECRET_ACCESS_KEY}
EOF

# Print the credentials file for debugging
cat ~/.aws/credentials

# Start the MLflow server
echo "Starting MLflow server..."
mlflow server --backend-store-uri $MLFLOW_TRACKING_URI --default-artifact-root s3://mlflow/ --host 0.0.0.0

echo "MLflow server exited with status $?"
