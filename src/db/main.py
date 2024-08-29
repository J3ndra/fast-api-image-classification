from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import settings

async_engine = create_async_engine(
    url = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        db=settings.POSTGRES_DB
    ),
    echo = True
)

async def init_db():
    async with async_engine.begin() as conn:
        from .models import Image
        await conn.run_sync(SQLModel.metadata.create_all)
        
async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session