from datetime import datetime
from fastapi import UploadFile
from pydantic import BaseModel, Field

class FileRequest(BaseModel):
    file_name: str = Field(..., min_length=1, max_length=100)
    file: UploadFile = Field(...)
    uploaded_at: datetime = Field(...) 

class FileResponse(BaseModel):
    id: int = Field(...)
    file_name: str = Field(..., min_length=1, max_length=100)
    file: UploadFile = Field(...)
    uploaded_at: datetime = Field(...) 

class FileDetailsRequest(BaseModel):
    file_name: str = Field(..., min_length=1, max_length=100)
    file_path: str = Field(..., min_length=1, max_length=100)
    stored_filename: str = Field(..., min_length=1, max_length=100)
    uploaded_at: datetime = Field(...)
    filesize: int = Field(..., le=10)
    content: str = Field(...)

class FileDetailsResponse(BaseModel):
    id: int = Field(...)
    file_name: str = Field(..., min_length=1, max_length=100)
    file_path: str = Field(..., min_length=1, max_length=100)
    stored_filename: str = Field(..., min_length=1, max_length=100)
    uploaded_at: datetime = Field(...)
    filesize: int = Field(..., le=10)
    content: str = Field(...)