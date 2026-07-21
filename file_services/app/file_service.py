from datetime import datetime
from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

import file_repository as repo
from .file_schemas import FileRequest, FileResponse

async def create_file(file_data: FileRequest, db: AsyncSession) -> FileResponse:
    """
    Creates and store a PDF file in the database.

    Validates that the file name is unique abd that the uploaded file is in PDF format. The file content is then read and stored in the database. Returns the details of the newly created file.

    Args:
        file_data (FileRequest): Request object containing the file name and uploaded PDF file.
        db (AsyncSession): SQLAlchemy asynchronous database session.
    
    Returns:
        FileResponse: Information about the stored file.

    Raises:
        HTTPException:
            - 409 Conflict: If a file with the same name already exists.
            - 400 Bad Request: Id the uploaded file is not a PDF.
            - 409 Conflict: If the file couldnot be created in the database.    
    """
    if await repo.get_file_by_filename(file_data.file_name, db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="File already exists.")
    
    if file_data.file.content_type != "application/pdf":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF Files are allowed.")
    
    pdf_byte = await file_data.file.read()
    result = await repo.create_file(file_data.file_name, pdf_byte, db)
    
    if not result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="File not created.")
    
    return result