from datetime import datetime
from sqlalchemy import select, LargeBinary
from sqlalchemy.ext.asyncio import AsyncSession

from .media_models import Media, MediaDetail
from .media_schemas import  MediaResponse,MediaDetailResponse

async def get_media_by_medianame(media_name: str, db: AsyncSession) -> MediaResponse | None:
    result = await db.execute(select(Media).where(Media.media_name == media_name))
    media = result.scalar_one_or_none()
    return media

async def add_media_file(media_name: str, media_bytes: LargeBinary, db: AsyncSession) -> MediaResponse | None:
    media = Media(
        media_name = media_name,
        media = media_bytes
    )

    db.add(media)
    await db.commit()
    await db.refresh(media)

    return media

async def add_media_details(media: MediaResponse, stored_name: str, media_path: str,media_size: int, media_type: str, uploaded_at: datetime, summary: str, db: AsyncSession) -> MediaDetailResponse:
    media_details = MediaDetail(
        media_id = media.id,
        media_name = media.media_name,
        stored_name = stored_name,
        media_path = media_path,
        media_size = media_size,
        media_type = media_type,
        uploaded_at = uploaded_at,
        summary = summary
    )

    db.add(media_details)
    await db.commit()
    await db.refresh(media_details)

    return media_details


async def rollback(db: AsyncSession):
    await db.execute(select(Media))
    await db.rollback()
    await db.execute(select(MediaDetail))
    await db.rollback()