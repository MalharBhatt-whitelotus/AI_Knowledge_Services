from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, LargeBinary, DateTime

from .media_database import Base

class Media(Base):
    __tablename__ = "medias"
    id = Column(Integer, primary_key=True)
    media_name = Column(String, nullable=False, index=True, unique=True)
    media = Column(LargeBinary, nullable=False)

class MediaDetail(Base):
    __tablename__ = "media_details"
    id = Column(Integer, primary_key=True)
    media_id = Column(Integer, nullable=False, index=True, unique=True)
    media_name = Column(String, nullable=False, index=True, unique=True)
    media_size = Column(Integer, nullable=False)
    media_type = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))