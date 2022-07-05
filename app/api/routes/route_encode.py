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

from app.models.schemas.file import(
    FileAdd,
    FileDetail
)


from app.api.deps import(
    allow_create_resource
)

from app.core.encoder import(
    encoderController,
    get_encoder_instance
)


router = APIRouter()



@router.post(
    '/create-encode',
    status_code=status.HTTP_200_OK,
    #dependencies=[Depends(allow_create_resource)]
)
async def create_upload_file(
    data: FileAdd,
    server: encoderController = Depends(get_encoder_instance)
):
    return get_encoder_instance().create_encode(source_id=data.source_id,
            serve_uri=data.serve_uri
        )
    
