from sqlalchemy import Column, String, Integer, LargeBinary, DateTime, Text

from .file_database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False, index=True)
    file = Column(LargeBinary, nullable=False)
    uploaded_at = Column(DateTime, nullable=False)

class FileDetail(Base):
    __tablename__ = "file_details"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, index=True, nullable=False, unique=True)
    file_name = Column(String, index=True, nullable=False)
    file_path = Column(String, nullable=False, unique=True)
    stored_filename= Column(String, nullable=False, index=True)
    uploaded_at = Column(DateTime, nullable=False)
    file_size = Column(Integer, nullable=False)
    content = Column(Text)
    summary = Column(String)