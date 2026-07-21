from fastapi import FastAPI

from .file_routes import file_routes as routes
from .file_config import settings

app = FastAPI(title=settings.APP_NAME,
              version=settings.APP_VERSION)

app.include_router(routes)