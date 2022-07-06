from fastapi import APIRouter
from app.api.routes import route_upload
from app.api.routes import route_encode
from app.api.routes import route_file


api_router = APIRouter()
api_router.include_router(route_upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(route_encode.router, prefix="/encode", tags=["encode"])
api_router.include_router(route_file.router, prefix="/file", tags=["file"])


