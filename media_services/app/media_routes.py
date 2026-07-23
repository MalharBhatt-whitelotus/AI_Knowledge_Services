from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, UploadFile, Depends

from .media_database import get_db
from .media_schemas import MediaDetailRequest, MediaDetailResponse

import media_services.app.media_services as service

media_router = APIRouter(prefix="/media", tags=["medias"])


@media_router.get("/health", status_code=200)
async def get_health():
    """
    Verify that the Media Service is running and reachable.

    ?Returns:
        dict: Service health status.
    """
    return {"status": "ok", "service": "media_service"}


@media_router.post("/upload",response_model=MediaDetailResponse)
async def upload_media(media_file: UploadFile, db: AsyncSession = Depends(get_db)):
    """
    Upload and store a new media record.
   
    Creates a new media entry in the database using the provided media information and returns the created media details.
    
    *Args:
        media_data (MediaRequest): Request body containing the media metadata.
        db (AsyncSession): SQLAlchemy asynchronous database session provided through dependency injection.
    
    ?Returns:
        MediaResponse: Details of the newly created media.
   
    !Raises:
        HTTPException: If the media cannot be created due to validation or
        database-related errors.
    """
    result = await service.create_media(media_file, db)
    return result


@media_router.delete("/delete/{id}",response_model=MediaDetailResponse)
async def delete_media(id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete and remove a existing media record.
    
    Deletes a old media entry in the database using the provided media information and returns the deleted media details.
    
    *Args:
        id (int): Request variable containing the media_details id.
        db (AsyncSession): SQLAlchemy asynchronous database session provided through dependency injection.
    
    ?Returns:
        MediaResponse: Details of the newly created media.
    
    !Raises:
        HTTPException: If the media cannot be created due to validation or
        database-related errors.
    """
    result = await service.delete_media(id, db)
    return result


@media_router.get("/get_all_details",response_model=list[MediaDetailResponse])
async def get_all_details(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all media records.

    Fetches and returns the details of all media files stored in the
    database.

    *Args:
        db (AsyncSession): SQLAlchemy asynchronous database session
            provided through dependency injection.

    ?Returns:
        list[MediaDetailResponse]: A list containing the details of all
        stored media files.

    !Raises:
        HTTPException: If an error occurs while retrieving the media
            details from the database.
    """
    media_details = await service.get_all_media_details(db)
    return media_details

@media_router.patch("/update/{id}", response_model=MediaDetailResponse)
async def update_media_details(id: int, details: MediaDetailRequest, db: AsyncSession = Depends(get_db)):
    """
    Update the details of an existing media record.

    Updates the metadata of the specified media file using the provided
    information and returns the updated media details.

    *Args:
        id (int): Unique identifier of the media record to update.
        details (MediaDetailRequest): Request body containing the updated
            media details.
        db (AsyncSession): SQLAlchemy asynchronous database session
            provided through dependency injection.

    ?Returns:
        MediaDetailResponse: The updated media details.

    !Raises:
        HTTPException:If an error occurs while retrieving the media
            details from the database.
    """
    result = await service.update_media_details(id, details, db)
    return result