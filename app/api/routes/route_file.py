import os
from typing import List
from sqlalchemy.orm import Session
from fastapi import(
    Depends,
    Response,
    status,
    APIRouter,
    File,
    UploadFile
)
from fastapi.responses import JSONResponse


from app.core.database import get_db

from app.models.domain.file import File


from app.api.deps import(
    allow_create_resource
)

from app.core.encoder import(
    encoderController,
    get_encoder_instance
)


router = APIRouter()



@router.post(
    '/statuses',
    status_code=status.HTTP_200_OK,
    #dependencies=[Depends(allow_create_resource)]
)
async def find_by_statuses(
    db: Session = Depends(get_db)
):
    return File.find_by_statuses(session=db, statuses=["PENDING_DOWNLOAD", "DOWNLOADING", "PENDING_ENCODE", "ENCODING", "DONE"])
    
