from fastapi import APIRouter

from app.api.endpoints import plans, storage

api_router = APIRouter()
api_router.include_router(plans.router, tags=["plans"])
api_router.include_router(storage.router, tags=["storage"])
