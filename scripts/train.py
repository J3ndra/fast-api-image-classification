import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
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
mlflow.set_experiment("Model Train")  # Set the MLflow experiment

# Directory paths
data_dir = 'datasets/preprocessed/'
model_dir = 'models/'

# Hyperparameters
img_size = (128, 128)
batch_size = 32
num_classes = 9

def load_data(data_dir, img_size, batch_size):
    """Load preprocessed image data from directory."""
    datagen = ImageDataGenerator(rescale=1.0/255.0)
    
    data = datagen.flow_from_directory(
        data_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical'
    )
    
    return data

def create_model(img_size, num_classes):
    """Create a basic CNN model."""
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(*img_size, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def train_model(data, model_dir):
    """Train the model and save it to model_dir."""
    mlflow.tensorflow.autolog()  # Automatically log metrics and model with MLflow
    
    model = create_model(img_size, num_classes)
    
    # Train the model
    history = model.fit(data, epochs=10, verbose=1)
    
    # Save the trained model
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    model_path = os.path.join(model_dir, 'model.h5')
    model.save(model_path)
    print(f"Model saved to {model_path}")
    
    # Manually log the model to MLflow
    mlflow.log_artifact(model_path, artifact_path="models")
    
if __name__ == "__main__":
    mlflow.start_run()  # Start an MLflow run
    
    data = load_data(data_dir, img_size, batch_size)
    train_model(data, model_dir)
    
    mlflow.end_run()  # End the MLflow run
