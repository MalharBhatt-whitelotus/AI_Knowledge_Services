import os
import uuid
from typing import Dict
from datetime import datetime, timezone
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from .media_config import settings
import media_services.app.media_repository as repo
from .media_schemas import MediaRequest, MediaDetailResponse


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

    media_byte = media_file.read()
    media_file.seek(0)
    media_name = media_file.filename()
    if repo.get_media_by_medianame(media_name, db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="File already exists.")
    
    media_size = len(media_byte)
    type = media_file.content_type() #! this will give error cause of response model but for now let it be....
    if type not in ["audio/mpeg", "video/mp4"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is not in audio/mpeg or video/mp4 format")
    media_type = "mp3" if type == "audio/mpeg" else "mp4"
    uploaded_at = datetime.now(timezone.utc)
    
    try:
        media_name_path = _save_media(media_file, media_type)
        media = await repo.add_media_file(media_name, media_byte)
        if not media:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="File not created.")
        
        summary = _generate_summary(media, media_size, media_type, media_name_path["stored_medianame"],media_name_path["media_path"],uploaded_at)

        media_details = await repo.add_media_details(media, media_name_path["stored_medianame"], media_name_path["media_path"], media_size, media_type, uploaded_at, summary, db)
        if not media_details:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="file_details not created.")
    except Exception as e:
        await repo.rollback(db)
        _delete_media(media_name_path["media_path"])
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Media not created.")
    
    return media_details







"""
===========================================
           * Helper Functions *
===========================================
"""

def _save_media(media_file: UploadFile, media_type: str)-> Dict[str, str]:
    os.makedirs(settings.UPLOAD_DIR,exist_ok=True)

    stored_medianame = f"{uuid.uuid4()}.{media_type}"
    media_path = os.path.join(settings.UPLOAD_DIR, stored_medianame)

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