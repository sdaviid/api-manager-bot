from fastapi import APIRouter
from app.api.routes import route_upload


api_router = APIRouter()
api_router.include_router(route_upload.router, prefix="/upload", tags=["upload"])
