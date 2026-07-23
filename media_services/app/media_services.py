import os
import uuid
import shutil
from typing import Dict
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, UploadFile

from .media_config import settings
import media_services.app.media_repository as repo
from .media_schemas import MediaRequest, MediaDetailRequest, MediaDetailResponse


"""
===========================================
        * Create Media Method *
===========================================
"""
async def create_media(media_file: UploadFile, db: AsyncSession) -> MediaDetailResponse:
    """
    Creates and store a mp3/mp4 media in the database.

    Validates that the media name is unique and that the uploaded media is in mp3/mp4 format. The media content is then read and stored in the database. Returns the details of the newly created media.

    *Args:
        media_data (MediaRequest): Request object containing the media name and uploaded mp3/mp4 media.
        db (AsyncSession): SQLAlchemy asynchronous database session.
    
    ?Returns:
        MediaDetailsResponse: Information about the stored media.

    !Raises:
        HTTPException:
            - 409 Conflict: If a media with the same name already exists.
            - 400 Bad Request: Id the uploaded media is not a mp3 nor a mp4.
            - 409 Conflict: If the media couldnot be created in the database.
            - 409 Conflict: If the media details couldnot be created in the database.
            - 409 Conflict: if either media or media_details is not stored in the database.    
    """
    try:
        media_byte = await media_file.read()
        await media_file.seek(0)
        media_name = media_file.filename

        if await repo.get_media_by_medianame(media_name, db):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="File already exists.")

        media_size = len(media_byte)

        media_type = settings.MEDIA_TYPES.get(media_file.content_type) 
        if media_type is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is not in audio/mpeg or video/mp4 format")
        uploaded_at = datetime.now(timezone.utc)

        media_name_path = _save_media(media_byte, media_type)
        media = await repo.add_media_file(media_name, media_byte, db)
        if not media:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="File not created.")
            
        summary = _generate_summary(media, media_size, media_type, media_name_path["stored_medianame"],media_name_path["media_path"],uploaded_at)

        media_details = await repo.add_media_details(media, media_name_path["stored_medianame"], media_name_path["media_path"], media_size, media_type, uploaded_at, summary, db)
        if not media_details:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="file_details not created.")
    except HTTPException:
        await repo.rollback(db)
        raise

    except OSError as exc:
        await repo.rollback(db)
        raise

    except Exception as e:
        await repo.rollback(db)
        _delete_media(media_name_path["media_path"])
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(e))
    
    return media_details


"""
===========================================
        * Delete Media Method *
===========================================
"""
async def delete_media(id: int, db: AsyncSession) -> MediaDetailResponse:
    """
    Delete and remove a existing media record.
    
    Deletes an old media entry in the database using the provided media information and returns the deleted media details.
    
    *Args:
        id (int): Request variable containing the media_details id.
        db (AsyncSession): SQLAlchemy asynchronous database session provided through dependency injection.
    
    ?Returns:
        MediaDetialResponse: Details of the deleted media.
    
    !Raises:
        HTTPException:
            - 404 Not Found: If the media file with same media id doesnot exists.
            - 404 Not Found: If the media_details with same id doesnot exists.
            - 409 Conflict: If the media not deleted from database nor from directory.
    """
    try:
        details = await repo.get_media_by_id(id, db)
        if not details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media details not found")

        if not await repo.get_media_by_medianame(details.media_name, db):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")
   
        await repo.delete_media_file(details.media_id, db)
        media_details = await repo.delete_media_details(id, db)
        _delete_media(media_details.media_path)
    except HTTPException:
        await repo.rollback(db)
        raise
    
    except Exception as e:
        await repo.rollback(db)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    return media_details


"""
===========================================
    * Get All Media Details Method *
===========================================
"""
async def get_all_media_details(db: AsyncSession) -> list[MediaDetailResponse]:
    """
    Retrive all media records.

    Fetches and returns the details of all media files stored in the database.

    *Args:
        db (AsyncSession): SQLAlchemy asynchronous database session.
    
    ?Returns:
        list[MediaDetailResponse]: A list containing the details of all stored media files.
    
    !Raises:
        HTTPException:
            - 404 Not Found: If any media details not exist.
    """
    try:
        media_details = await repo.get_all_media_details(db)
        if not media_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media details not exists.")
    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(exc))
    
    return media_details


async def update_media_details(id: int, details: MediaDetailRequest, db: AsyncSession):
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
        HTTPException:
            - 404 Not Found: If the specified media record does not exist.
            - 409 Conflict: If the media details are not updated in the database.
    """
    if not await repo.get_media_by_id(id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media details not found.")

    try: 
        media_details = await repo.update_media_details(id, details, db)
        if not media_details:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Media details not updated.")

        media = await repo.update_media_file(media_details, db)
        if not media:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Media not updated..")
    except HTTPException:
        await repo.rollback(db)
        raise

    except Exception as exc:
        await repo.rollback(db)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(exc))
    
    return media_details    



"""
===========================================
           * Helper Functions *
===========================================
"""

def _save_media(media_bytes: bytes, media_type: str)-> Dict[str, str]:
    os.makedirs(settings.UPLOAD_DIR,exist_ok=True)

    stored_medianame = f"{uuid.uuid4()}.{media_type}"
    media_path = os.path.join(settings.UPLOAD_DIR, stored_medianame)

    with open(media_path, "wb") as buffer:
        buffer.write(media_bytes)
    return {"stored_medianame": stored_medianame, "media_path": media_path}

def _delete_media(media_path: str) -> bool:
    if os.path.exists(media_path):
        if os.remove(media_path):
            return True
    return False

def _generate_summary(media_detials: MediaRequest,media_size: int, media_type: str, stored_medianame: str, media_path: str, uploaded_at: datetime) -> str:
    summary = ""

    summary += f"The document is named {media_detials.media_name}."
    summary += f" And it is stored as {stored_medianame}."
    summary += f" It is stored at {media_path}"
    summary += f" It is a {media_type} document."
    summary += f" The file size is {media_size}."
    summary += f" It was uploaded on {uploaded_at}."
    summary += " Text has been successfully extracted and is available for AI-based querying."
    summary += f"{'-'*30}\nTHE CONTENTS OF THE FILE ARE:\n{'-'*30}\n{media_detials.media}"

    return summary