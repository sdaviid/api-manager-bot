import requests
from app.core.controller_auth import controller_instance

from app.models.domain.file import File
from app.core.database import SessionLocal

from app.config import SERVER_UPLOADER

class uploaderController(object):
    def __init__(self, controller_instance):
        self.controller_instance = controller_instance
    def gen_token(self):
        return self.controller_instance.create_token('cli-web-uploader')
    def upload(self, serve_uri):
        try:
            token = self.gen_token()
            if token:
                headers = {
                    'Authorization': f'Bearer {token}'
                }
                payload = {
                    'origin': serve_uri
                }
                response = requests.post(f'{SERVER_UPLOADER}/file/upload', json=payload, headers=headers)
        except Exception as err:
            print(f'uploaderController.upload exception - {err}')



uploader_instance = uploaderController(controller_instance=controller_instance)

def get_uploader_instance():
    return uploader_instance
