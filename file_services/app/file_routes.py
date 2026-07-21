from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, status, Depends

import file_service as service
from .file_database import get_db
from .file_schemas import FileRequest, FileResponse

file_router = APIRouter(prefix="/file", tags=["files"])

@file_router.get("/health", status_code=200)
async def health_check():
    return {"status":"ok","service":"file_services"}

@file_router.post("/upload", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(file_data: FileRequest, db: AsyncSession = Depends(get_db)):
    """
    Upload and store a new file record.

    Creates a new file entry in the database using the provided file
    information and returns the created file details.

    Args:
        file_data (FileRequest): Request body containing the file metadata.
        db (AsyncSession): SQLAlchemy database async session provided through dependency injection.

    Returns:
        FileResponse: Details of the newly created file.

    Raises:
        HTTPException: If the file cannot be created due to validation or
        database-related errors.
    """
    result = await service.create_file(file_data = file_data, db = db)
    return result