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

#from utils.encode import(
#    hash_torrent
#)


from app.core.database import get_db

from app.api.deps import(
    allow_create_resource
)

from app.core.torrent import(
    torrentController,
    get_torrent_instance
)


router = APIRouter()



@router.post(
    '/upload',
    status_code=status.HTTP_200_OK,
    #dependencies=[Depends(allow_create_resource)]
)
async def create_upload_file(
    file: UploadFile,
    server: torrentController = Depends(get_torrent_instance)
):
    contents = await file.read()
    path_file = os.path.join(os.getcwd(), 'files', file.filename)
    if os.path.isfile(path_file) == False:
        with open(path_file, 'wb') as f:
            f.write(contents)
    data_upload = server.upload_torrent(path_file)
    return data_upload
    
