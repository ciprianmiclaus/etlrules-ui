from fastapi import APIRouter

from app.api.endpoints import plans, folders

api_router = APIRouter()
api_router.include_router(plans.router, tags=["plans"])
api_router.include_router(folders.router, tags=["folders"])
