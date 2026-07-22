from datetime import datetime
from sqlalchemy import LargeBinary, select
from sqlalchemy.ext.asyncio import AsyncSession

from .file_models import File, FileDetail
from .file_schemas import FileResponse, FileDetailsRequest, FileDetailsResponse

@staticmethod
async def create_file(
        file_name: str, 
        file: LargeBinary, 
        uploaded_at: datetime, 
        db: AsyncSession
        ) -> FileResponse:
    
    file = File(
        file_name = file_name,
        file = file,
        uploaded_at = uploaded_at
        )
    
    db.add(file)
    await db.commit()
    await db.refresh(file)

    return file

@staticmethod
async def get_file_by_filename(
        file_name: str, 
        db: AsyncSession
        ) -> FileResponse | None:
    
    result = await db.execute(select(File).where(File.file_name == file_name))
    file = result.scalar_one_or_none()

    return file

@staticmethod
async def add_file_details(
        file_id: int,
        file_name: str, 
        file_path: str, 
        stored_filename: str, 
        uploaded_at: datetime, 
        file_size: int, 
        content: str,
        summary:str, 
        db: AsyncSession
        ) -> FileDetailsResponse:
    
    file_details = FileDetail(
        file_id = file_id,
        file_name = file_name,
        file_path = file_path,
        stored_filename = stored_filename,
        uploaded_at = uploaded_at,
        file_size = file_size,
        content = content,
        summary = summary
    )

    db.add(file_details)
    await db.commit()
    await db.refresh(file_details)

    return file_details

@staticmethod
async def get_file_detials_by_filename(
        filename: str, 
        db: AsyncSession
        ) -> FileDetailsResponse | None:
    
    result = await db.execute(select(FileDetail).where(FileDetail.file_name == filename))
    file = result.scalar_one_or_none()
    
    return file

@staticmethod
async def get_file_by_id(file_id: int, db: AsyncSession) -> FileResponse:
    result = await db.execute(select(File).where(File.id == file_id))
    file = result.scalar_one_or_none()
    return file 

@staticmethod
async def get_file_details_by_id(id: int, db: AsyncSession) -> FileDetailsResponse | None:
    result = await db. execute(select(FileDetail).where(FileDetail.id == id))
    file_details = result.scalar_one_or_none()
    return file_details

@staticmethod
async def delete_file(file_id: int, db: AsyncSession) -> FileResponse:
    result = await db.execute(select(File).where(File.id == file_id))
    file = result.scalar_one_or_none()
    
    await db.delete(file)
    await db.commit()

    return file

@staticmethod
async def delete_file_details(id: int, db: AsyncSession) -> FileDetailsResponse:
    result = await db.execute(select(FileDetail).where(FileDetail.id == id))
    file_details = result.scalar_one_or_none()
    
    await db.delete(file_details)
    await db.commit()
    
    return file_details

@staticmethod
async def get_details_of_all_files(db: AsyncSession) -> list[FileDetailsResponse]:
    result = await db.execute(select(FileDetail))
    details = result.scalars().all()

    return details

@staticmethod
async def update_file_details(id: int, details: FileDetailsRequest, db: AsyncSession) -> FileDetailsResponse:

    result = await db.execute(select(FileDetail).where(FileDetail.id == id))
    file_details = result.scalar_one_or_none()

    file_details.id = id
    file_details.file_id = details.file_id
    file_details.file_name = details.file_name
    file_details.file_path = details.file_path
    file_details.stored_filename = details.stored_filename
    file_details.uploaded_at = details.uploaded_at
    file_details.file_size = details.file_size
    file_details.content = details.content
    file_details.summary = details.summary

    await db.commit()
    await db.refresh(file_details)

    return file_details



"""
===========================================
            *Helper Functions*
===========================================
"""

@staticmethod
async def rollback(db: AsyncSession):
    await db.execute(select(File))
    await db.rollback()
    await db.execute(select(FileDetail))
    await db.rollback()