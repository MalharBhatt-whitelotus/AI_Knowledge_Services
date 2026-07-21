from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from file_services.app.file_config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
sessionLocal =  sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()