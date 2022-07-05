from fastapi import APIRouter
from app.api.routes import route_upload
from app.api.routes import route_encode


api_router = APIRouter()
api_router.include_router(route_upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(route_encode.router, prefix="/encode", tags=["encode"])

