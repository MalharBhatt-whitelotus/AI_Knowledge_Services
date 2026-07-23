from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class MediaSettings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    DATABASE_URL: str
    UPLOAD_DIR: str
    MEDIA_TYPES: dict[str, str]

    model_config = SettingsConfigDict(
        env_file= BASE_DIR / ".env",
        extra="ignore"
        )

settings = MediaSettings()