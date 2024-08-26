from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.images.routes import image_router
from src.utils.initialize_minio_client import initialize_minio_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ Starting application")
    
    await init_db()
    
    '''
    Initialize minio client
    '''
    app.state.minio_client = initialize_minio_client()
    
    yield
    print("⛔ Stopping application")

app = FastAPI(
    title="Skin Cancer Classification API",
    version="0.1",
    description="This is a simple image classification for skin cancer API",
    lifespan=lifespan
)

app.include_router(image_router, tags=['images'])
