from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, status, UploadFile, Depends

import file_services.app.file_service as service
from .file_database import get_db
from .file_schemas import FileRequest, FileResponse, FileDetailsRequest, FileDetailsResponse

file_router = APIRouter(prefix="/file", tags=["files"])

@file_router.get("/health", status_code=200)
async def health_check():
    return {"status":"ok","service":"file_services"}

@file_router.post("/upload", response_model=FileDetailsResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile, db: AsyncSession = Depends(get_db)) -> FileDetailsResponse:
    """
    Upload and store a new file record.

    Creates a new file entry in the database using the provided file
    information and returns the created file details.

    *Args:
        file_data (FileRequest): Request body containing the file metadata.
        db (AsyncSession): SQLAlchemy asynchronous database session provided through dependency injection.

    ?Returns:
        FileResponse: Details of the newly created file.

    !Raises:
        HTTPException: If the file cannot be created due to validation or
        database-related errors.
    """
    result = await service.create_file(file_data = file, db = db)
    return result

@file_router.delete("/delete/{id}", status_code=200)
async def delete_file(id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete and remove the old file record.

    Removes the required file entry in the database using the provided file information and returns the deleted file details.

    *Args:
        id (int): Request variable containing the file ID.
        db (AsyncSession): SQLAlchemy asynchronous database session provided through dependency injection.

    ?Returns:
        FileDetailsResponse: Details of the deleted file.
    
    !Raises:
        HTTPException: If the file cannot be created due to validation or database-realated errors.
    """
    result = await service.delete_file(id, db)
    return result

@file_router.get("/get_details/of_all_files", response_model=list[FileDetailsResponse])
async def get_details_of_all_files(db: AsyncSession = Depends(get_db)):
    """
    Get details of the stored files.

    Fetch the list of all details of the files from the database and returns the list of file details.

    *Args:
        db (AsyncSession): SQLAlchemy asynchronous database session provided through dependency injection.
    
    ?Returns:
        details (List[FileDetailsResponse]): Details of all the stored files.

    !Raises:
        HTTPEXception: If the file details cannot be fetched due to validation or database-related errors.
    """
    details = await service.get_details_of_all_files(db)
    return details

@file_router.patch("/update_details/{id}", response_model=FileDetailsResponse)
async def update_file_details(
    id: int, 
    details: FileDetailsRequest, 
    db: AsyncSession = Depends(get_db)
    ):
    """
    Update the details of file in the database.

    Update the required file entry in the database using the provided file information and returns the details of the updated file.

    *Args:
        id (int): Request variable containing file_detail ID.
        details (FileDetailsRequest): Request Body containing file updated details.
        db (AsnycSession): SQLAlchemy asynchronous database session provided through dependency injection.

    ?Returns:
        response (FileDetailsResponse): Record of the updated file_details.
    
    !Raises:
        HTTPException: If the file details cannot be updated due to validation or database-related errors.
    """
    response = await service.update_file_details(id, details, db)
    return response