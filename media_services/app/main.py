from fastapi import FastAPI

from .media_routes import media_router

app = FastAPI()

app.include_router(media_router)