import os
import fitz
import uuid
import shutil
import pymupdf
from datetime import datetime
from typing import Any, Dict
from fastapi import HTTPException, status, UploadFile

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

import file_repository as repo
from .file_schemas import FileRequest, FileDetailsResponse
from .file_config import settings


"""
===========================================
            *Create File Method*
===========================================
"""
async def create_file(file_data: FileRequest, db: AsyncSession) -> FileDetailsResponse:
    """
    Creates and store a PDF file in the database.

    Validates that the file name is unique and that the uploaded file is in PDF format. The file content is then read and stored in the database. Returns the details of the newly created file.

    Args:
        file_data (FileRequest): Request object containing the file name and uploaded PDF file.
        db (AsyncSession): SQLAlchemy asynchronous database session.
    
    Returns:
        FileDetailsResponse: Information about the stored file.

    Raises:
        HTTPException:
            - 409 Conflict: If a file with the same name already exists.
            - 400 Bad Request: Id the uploaded file is not a PDF.
            - 409 Conflict: If the file couldnot be created in the database.
            - 409 Conflict: If a file with the same name already exists in the details.    
    """
    if await repo.get_file_by_filename(file_data.file_name, db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="File already exists.")
    
    if file_data.file.content_type != "application/pdf":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF Files are allowed.")
    
    pdf_byte = await file_data.file.read()
    uploaded_at = datetime.now()
    result = await repo.create_file(file_data.file_name, pdf_byte, uploaded_at, db)
    
    if not result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="File not created.")
    
    file_detail = _fetch_file_details(file_data)
    summary = _generate_summary(file_data.file_name, 
        file_detail["file_path"], 
        file_detail["stored_filename"], 
        uploaded_at, 
        file_detail["file_size"], 
        file_detail["content"])
    if await repo.get_file_detials_by_filename(file_detail["stored_filename"]):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="File details already exist.")
    file_details = await repo.add_file_details(
        result.id,
        file_data.file_name, 
        file_detail["file_path"], 
        file_detail["stored_filename"], 
        uploaded_at, 
        file_detail["file_size"], 
        file_detail["content"],
        summary, 
        db
        )
    
    return file_details


"""
===========================================
            *Delete File Method*
===========================================
"""
async def delete_file(id: int, db: AsyncSession) -> FileDetailsResponse:
    """
    Deletes a PDF file from the database and also from the Directory.

    Validates that the file exists in database as well as in the directory. The file is then read and deleted from the database and from the directory. Returns the details of the deleted file.

    Args:
        id (int): Request object containing the file ID.
        db (AsyncSession): SQLAlchemy asynchronous database session.
    
    Returns:
        FileDetailsResponse: Information about the deleted file.

    Raises:
        HTTPException:
            - 404 Not Found: If a file with the same file id doesnot exists.
            - 404 Not Found: If the file details with the same id doesnot exists.
            - 501 Not Implemented: If the file or file details are not deleted.  
    """

    file_details = await repo.get_file_details_by_id(id, db)

    if not await file_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
    
    file_id = file_details["file_id"]

    if not await repo.get_file_by_id(file_id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File details not found.")
    
    try:
        await repo.delete_file(file_id, db)
        deleted_file_details = await repo.delete_file_details(id, db)
    except:
        await repo.rollback()
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="File not deleted.")

    return deleted_file_details | None 



"""
===========================================
            *Helper Functions*
===========================================
"""
def _fetch_file_details(file: UploadFile) -> Dict[str: Any]:
    file_details = _save_file(file)
    file_path = file_details["filepath"]
    stored_filename = file_details["stored_filename"]

    content = _extract_text(file)
    filesize = _get_file_size(file_path)

    return {
        "file_path": file_path,
        "stored_filename": stored_filename,
        "file_size": filesize,
        "content": content
        }

def _save_file(file: UploadFile) -> Dict[str: str]:
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    filename = f"{uuid.uuid4()}.pdf"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"stored_filename": filename, "filepath": filepath}

def _get_file_size(filepath: str) -> int:
    size = os.path.getsize(filepath)
    return size

def _extract_text(file) -> str:
    text = ""
    doc = pymupdf.open(file)
    for page in doc:
        text += page.get_text()
    return text

def _generate_summary(
        file_name: str,
        file_path: str,
        stored_filename: str,
        uploaded_at: datetime,
        file_size: int,
        content: str
) -> str:
    summary = ""

    # Basic Information
    summary += f"The document is named {file_name}."
    summary += f" And it is stored as {stored_filename}."
    summary += f" It is stored at {file_path}"
    summary += " It is a PDF document."
    summary += f" The file size is {file_size}."
    summary += f" It was uploaded on {uploaded_at}."
    summary += " Text has been successfully extracted and is available for AI-based querying."
    summery += f"{'-'*30}\nTHE CONTENTS OF THE FILE ARE:\n{'-'*30}\n{content}"