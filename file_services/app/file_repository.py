from datetime import datetime
from sqlalchemy import LargeBinary, select
from sqlalchemy.ext.asyncio import AsyncSession

from .file_models import File
from .file_schemas import FileResponse

async def create_file(
        file_name: str, 
        file: LargeBinary, 
        uploaded_at: datetime, 
        db: AsyncSession
        ) -> FileResponse:
    
    file = File(
        file_name=file_name,
        file=file,
        uploaded_at=uploaded_at
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