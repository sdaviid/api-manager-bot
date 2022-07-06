import requests
from app.core.controller_auth import controller_instance

from app.models.domain.file import File
from app.core.database import SessionLocal

from app.config import SERVER_ENCODER

class encoderController(object):
    def __init__(self, controller_instance):
        self.controller_instance = controller_instance
    def gen_token(self):
        return self.controller_instance.create_token('cli-web-encoder')
    def create_encode(self, source_id, serve_uri):
        try:
            token = self.gen_token()
            if token:

                headers = {
                    'Authorization': f'Bearer {token}'
                }
                payload = {
                    'url': serve_uri
                }
                response = requests.post(f'{SERVER_ENCODER}/file/add', json=payload, headers=headers)
                if response.status_code == 200:
                    return response.json()
        except Exception as err:
            print(f'encoderController.create_encode exception - {err}')
        return False
    def get_data_by_hash(self, hash):
        try:
            token = self.gen_token()
            if token:
                headers = {
                    'Authorization': f'Bearer {token}'
                }
                response = requests.get(f'{SERVER_ENCODER}/file/status/{hash}', headers=headers)
                if response.status_code == 200:
                    return response.json()
        except Exception as err:
            print(f'encoderController.get_data_by_hash exception - {err}')
        return False


encoder_instance = encoderController(controller_instance=controller_instance)

def get_encoder_instance():
    return encoder_instance