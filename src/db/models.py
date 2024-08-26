from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime

class Image(SQLModel, table=True):
    __tablename__ = "images"
    uid: UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, unique=True, default=uuid4)
    )
    filename: str
    file_path: str
    prediction: str
    prediction_confidence: float
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    def __repr__(self) -> str:
        return f"Image => {self.filename}"