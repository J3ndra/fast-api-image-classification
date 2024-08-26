from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi import Depends
from minio import Minio
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from src.config import settings
from src.images.schemas import ImageCreateModel, ImageResponseModel, PredictionResponseModel
from src.images.services import ImageServices
from src.utils.get_minio_client import get_minio_client

image_router = APIRouter(
    prefix="/api/images",
)

@image_router.get("/")
async def read_images():
    return {"message": "Read all images"}

@image_router.get("/{image_id}")
async def read_image(
    image_id: str,
    session: AsyncSession = Depends(get_session),
    minio_client: Minio = Depends(get_minio_client)
):
    image_service = ImageServices(session, minio_client)
    image = await image_service.get_image(image_id)
    
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return image_service.generate_presigned_url(image)

@image_router.post("/test-upload", response_model=ImageResponseModel)
async def test_upload_image(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    minio_client: Minio = Depends(get_minio_client)
):
    service = ImageServices(session, minio_client)
    image_create = ImageCreateModel(image=file)
    image = await service.upload_image(image_create, settings.MINIO_BUCKET)
    return image

@image_router.post("/predict", response_model=PredictionResponseModel)
async def predict_image(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    minio_client: Minio = Depends(get_minio_client)
):
    service = ImageServices(session, minio_client)
    image_create = ImageCreateModel(image=file)
    prediction = await service.predict_image(image_create, settings.MINIO_BUCKET)
    return prediction