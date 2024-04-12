from fastapi import FastAPI

from app.api import router as api_router
from app.config import settings

# Initialize FastAPI application
app = FastAPI(title=settings.app_name, debug=settings.debug)

# Include API router with '/api' prefix
app.include_router(api_router, prefix="/api")
