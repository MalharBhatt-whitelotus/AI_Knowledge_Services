from sqlalchemy import Enum, LargeBinary
from datetime import datetime
from pydantic import BaseModel, Field

class MediaType(str, Enum):
    mp3 = "mp3"
    mp4 = "mp4"

class MediaRequest(BaseModel):
    id: int = Field(...)
    media_name: str = Field(..., min_length=1, max_length=100)
    media: LargeBinary = Field(...)

class MediaResponse(BaseModel):
    id: int
    media_name: str 
    media: LargeBinary 

class MediaDetailRequest(BaseModel):
    id: int = Field(...)
    media_id: int = Field(...)
    media_name: str = Field(..., min_length=1, max_length=100)
    media_size: int = Field(..., le=10)
    media_type: MediaType = Field(...)
    uploaded_at: datetime = Field(...)
    summary: str = Field(...)

class MediaDetailResponse(BaseModel):
    id: int
    media_id: int
    media_name: str
    media_size: int
    media_type: MediaType
    uploaded_at: datetime
    summary: str