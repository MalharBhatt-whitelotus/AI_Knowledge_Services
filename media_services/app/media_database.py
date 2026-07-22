from sqlalchemy import NullPool, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine 
from sqlalchemy.orm import sessionmaker, declarative_base

from .media_config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo = True,
    poolclass = NullPool
    )

sessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()

async def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        await db.close()