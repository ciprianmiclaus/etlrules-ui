from fastapi import APIRouter

from app.api.endpoints import plans

api_router = APIRouter()
api_router.include_router(plans.router, tags=["plans"])
