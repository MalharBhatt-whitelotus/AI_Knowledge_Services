from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from file_services.app.file_config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    poolclass=NullPool
    )
sessionLocal =  sessionmaker(
    bind=engine, 
    autocommit=False, 
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False
    )
Base = declarative_base()

async def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        await db.close()