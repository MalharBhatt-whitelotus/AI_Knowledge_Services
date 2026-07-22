from datetime import datetime
from sqlalchemy import LargeBinary, select
from sqlalchemy.ext.asyncio import AsyncSession

from .file_models import File, FileDetail
from .file_schemas import FileResponse, FileDetailsResponse


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


async def get_file_by_filename(
        file_name: str, 
        db: AsyncSession
        ) -> FileResponse | None:
    
    result = await db.execute(select(File).where(File.file_name == file_name))
    file = result.scalar_one_or_none()

    return file


async def add_file_details(
        file_id: int,
        file_name: str, 
        file_path: str, 
        stored_filename: str, 
        uploaded_at: datetime, 
        file_size: int, 
        content: str, 
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
    )

    db.add(file_details)
    await db.commit()
    await db.refresh(file_details)

    return file_details


async def get_file_detials_by_filename(
        filename: str, 
        db: AsyncSession
        ) -> FileDetailsResponse | None:
    
    result = await db.execute(select(FileDetail).where(FileDetail.file_name == filename))
    file = result.scalar_one_or_none()
    
    return file


async def get_file_by_id(file_id: int, db: AsyncSession) -> FileResponse:
    result = await db.execute(select(File).where(File.id == file_id))
    file = result.scalar_one_or_none()
    return file 


async def get_file_details_by_id(id: int, db: AsyncSession) -> FileDetailsResponse | None:
    result = await db. execute(select(FileDetail).where(File.id == id))
    file_details = result.scalar_one_or_none()
    return file_details


async def delete_file(file_id: int, db: AsyncSession) -> FileResponse:
    result = await db.execute(select(File).where(File.id == file_id))
    file = result.scalar_one_or_none()
    
    db.delete(file)
    await db.commit()

    return file

async def delete_file_details(id: int, db: AsyncSession) -> FileDetailsResponse:
    result = await db.execute(select(FileDetail).where(FileDetail.id == id))
    file_details = result.scalar_one_or_none()
    
    db.delete(file_details)
    await db.commit()
    
    return file_details


async def get_details_of_all_files(db: AsyncSession) -> list[FileDetailsResponse]:
    result = await db.execute(select(FileDetail))
    details = result.scalars().all()

    return details


"""
===========================================
            *Helper Functions*
===========================================
"""
async def rollback(db: AsyncSession):
    await db.rollback()