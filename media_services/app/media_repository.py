from datetime import datetime
from sqlalchemy import select, LargeBinary, text, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import BackgroundTasks
from .media_models import Media, MediaDetail
from .media_schemas import  MediaResponse, MediaDetailRequest, MediaDetailResponse


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
        stored_medianame = stored_name,
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


async def get_media_by_id(id: int, db: AsyncSession) -> MediaDetailResponse | None:
    result = await db.execute(select(MediaDetail).where(MediaDetail.id == id))
    media_details = result.scalar_one_or_none()
    return media_details


async def delete_media_file(media_id: int, db: AsyncSession) -> MediaResponse:
    result = await db.execute(select(Media).where(Media.id == media_id))
    media = result.scalar_one_or_none()
    await db.delete(media)
    await db.commit()

    await reset_id_media(db, "medias")

    return media


async def delete_media_details(id: int, db: AsyncSession) -> MediaDetailResponse:
    result = await db.execute(select(MediaDetail).where(MediaDetail.id == id))
    media_details = result.scalar_one_or_none()
    await db.delete(media_details)
    await db.commit()

    await reset_id_media(db, "media_details")

    return media_details


async def get_all_media_details(db: AsyncSession)-> list[MediaDetailResponse]:
    result = await db.execute(select(MediaDetail))
    media_details = result.scalars().all()
    return media_details


async def update_media_details(id: int, details: MediaDetailRequest, db: AsyncSession) -> MediaDetailResponse:
    result = await db.execute(select(MediaDetail).where(MediaDetail.id == id))
    media_details = result.scalar_one_or_none()
    media_details.id = id
    media_details.media_id = details.media_id
    media_details.media_name = details.media_name
    media_details.stored_medianame = details.stored_medianame
    media_details.media_path = details.media_path
    media_details.media_size = details.media_size
    media_details.media_type = details.media_type
    media_details.uploaded_at = details.uploaded_at
    media_details.uploaded_at = details.uploaded_at

    await db.commit()
    await db.refresh(media_details)
    return media_details


async def update_media_file(media_details: MediaDetailResponse, db: AsyncSession) -> MediaResponse:
    result = await db.execute(select(Media).where(Media.id == media_details.media_id))
    media = result.scalar_one_or_none()
    media.id = media_details.media_id
    media.media_name = media_details.media_name

    await db.commit()
    await db.refresh(media)

    return media





"""
===========================================
           * Helper Functions *
===========================================
"""


async def rollback(db: AsyncSession):
    await db.execute(select(Media))
    await db.rollback()
    await db.execute(select(MediaDetail))
    await db.rollback()

async def reset_id_media(db: AsyncSession, table_name) -> None:
    if table_name == "medias":
        count = await db.scalar(select(func.count()).select_from(Media))
    if table_name == "media_details":
        count = await db.scalar(select(func.count()).select_from(MediaDetail))

    if count == 0:
        await db.execute(text(f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1"))
        await db.commit()