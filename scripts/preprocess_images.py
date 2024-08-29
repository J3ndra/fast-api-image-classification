import os
from PIL import Image
import boto3
from botocore.client import Config
import mlflow
import mlflow.tensorflow

# Set MinIO credentials (use the root user and password defined in docker-compose)
os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID", "minioadmin")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY", "minioadminpassword")
os.environ["MLFLOW_S3_ENDPOINT_URL"] = os.getenv("MLFLOW_S3_ENDPOINT_URL", "http://localhost:12001")

# Configure boto3 session explicitly
session = boto3.session.Session(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
)

s3_client = session.client(
    service_name='s3',
    endpoint_url=os.environ["MLFLOW_S3_ENDPOINT_URL"],
    config=Config(signature_version='s3v4'),
)

mlflow.set_tracking_uri("http://localhost:12003")  # Set the MLflow tracking URI
mlflow.set_experiment("Preprocessing Image")  # Set the MLflow experiment

# Input and output directories
input_dir = 'datasets/images/'
output_dir = 'datasets/preprocessed/'
image_size = (128, 128)  # Resize images to 128x128 pixels

def preprocess_image(image_path, output_path):
    """Resize the image and save it to the output path."""
    try:
        img = Image.open(image_path)
        img = img.resize(image_size)
        img.save(output_path)
        print(f"Processed {output_path}")
        mlflow.log_artifact(output_path)  # Log the preprocessed image as an artifact
    except Exception as e:
        print(f"Failed to process {image_path}: {e}")

def preprocess_images(input_dir, output_dir):
    """Preprocess all images from input_dir, preserving subdirectory structure."""
    # Start an MLflow run
    with mlflow.start_run():
        for root, _, files in os.walk(input_dir):
            # Calculate the relative path to preserve subdirectory structure
            relative_path = os.path.relpath(root, input_dir)
            # Create the corresponding directory in the output path
            output_subdir = os.path.join(output_dir, relative_path)
            
            if not os.path.exists(output_subdir):
                os.makedirs(output_subdir)
            
            for img_name in files:
                input_path = os.path.join(root, img_name)
                output_path = os.path.join(output_subdir, img_name)
                
                # Process only files that are images
                if img_name.lower().endswith((".jpg", ".png", ".jpeg", ".bmp")):
                    preprocess_image(input_path, output_path)
                else:
                    print(f"Skipping non-image file: {input_path}")

if __name__ == "__main__":
    preprocess_images(input_dir, output_dir)
