from fastapi import APIRouter

from app.api.endpoints.calculate import router as calculate_router

router = APIRouter()

router.include_router(calculate_router)
