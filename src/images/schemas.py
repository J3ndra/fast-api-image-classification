from fastapi import UploadFile
from pydantic import BaseModel
from uuid import UUID

class ImageResponseModel(BaseModel):
    uid: UUID
    filename: str
    file_path: str
    prediction: str
    prediction_confidence: float

class ImageCreateModel(BaseModel):
    image: UploadFile

class PredictionResponseModel(BaseModel):
    file_path: str
    prediction: str
    confidence: float
