from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, UploadFile, Depends

import media_services.app.media_services as service

from .media_database import get_db
from .media_schemas import MediaDetailRequest, MediaDetailResponse

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