import io
import datetime
import numpy as np
from uuid import uuid4
from minio import Minio
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Image
from src.images.schemas import ImageCreateModel, ImageResponseModel, PredictionResponseModel
from src.config import settings
from tensorflow.keras.models import load_model # type: ignore
from src.utils.preprocess_image import preprocess_image

CLASS_NAMES = [
    "actinic keratosis",
    "basal cell carcinoma",
    "dermatofibroma",
    "melanoma",
    "nevus",
    "pigmented benign keratosis",
    "seborrheic keratosis",
    "squamous cell carcinoma",
    "vascular lesion"
]

class ImageServices:
    def __init__(self, session: AsyncSession, minio_client: Minio):
        self.session = session
        self.minio_client = minio_client
        self.model = load_model("src/model/my_keras_model2.keras")  # Load your model here
        
    async def get_image(self, image_id: str) -> Image:
        image = await self.session.get(Image, image_id)
        return image
    
    def generate_presigned_url(self, image: Image) -> ImageResponseModel:
        presigned_url = self.minio_client.presigned_get_object(
            bucket_name=settings.MINIO_BUCKET,
            object_name=image.file_path.split("/")[-1],
            expires=datetime.timedelta(days=1)
        )
        return ImageResponseModel(
            uid=image.uid,
            filename=image.filename,
            file_path=presigned_url,
            prediction=image.prediction,
            prediction_confidence=image.prediction_confidence
        )
        
    async def upload_image(self, image_create: ImageCreateModel, bucket_name: str) -> Image:
        file = image_create.image
        filename = f"{uuid4()}_{file.filename}"
        file_path = f"{bucket_name}/{filename}"

        # Read file contents
        contents = await file.read()

        # Wrap contents in a BytesIO object
        contents_io = io.BytesIO(contents)
        
        # Upload file to MinIO
        self.minio_client.put_object(bucket_name, filename, contents_io, len(contents))

        # Store metadata in PostgreSQL
        new_image = Image(
            uid=uuid4(),
            filename=file.filename,
            file_path=f"http://{settings.MINIO_ENDPOINT}/{file_path}",
            prediction="",
            prediction_confidence=0.0,
            created_at=datetime.datetime.now(),
        )
        self.session.add(new_image)
        await self.session.commit()

        return new_image
    
    async def predict_image(self, image_create: ImageCreateModel, bucket_name: str) -> PredictionResponseModel:
        file = image_create.image
        filename = f"{uuid4()}_{file.filename}"
        file_path = f"{bucket_name}/{filename}"

        # Read and preprocess the image
        contents = await file.read()
        contents_io = io.BytesIO(contents)
        image = preprocess_image(contents_io, target_size=(176, 176))  # Resizing to 176x176 as expected by the model

        # Perform prediction
        predictions = self.model.predict(image)
        predicted_class_index = np.argmax(predictions, axis=1)[0]
        confidence = float(np.max(predictions))

        # Map predicted class index to class name
        predicted_class_name = CLASS_NAMES[predicted_class_index]

        # Reset stream pointer before uploading to Minio
        contents_io.seek(0)

        # Store the image in MinIO
        self.minio_client.put_object(bucket_name, filename, contents_io, len(contents))

        # Create and save the Image record in the database
        new_image = Image(
            uid=uuid4(),
            filename=file.filename,
            file_path=f"http://{settings.MINIO_ENDPOINT}/{file_path}",
            prediction=predicted_class_name,
            prediction_confidence=confidence,
            created_at=datetime.datetime.now(),
        )
        self.session.add(new_image)
        await self.session.commit()

        # Return prediction response
        return PredictionResponseModel(
            file_path=f"http://{settings.MINIO_ENDPOINT}/{file_path}",
            prediction=predicted_class_name,
            confidence=confidence
        )