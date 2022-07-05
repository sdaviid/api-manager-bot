import requests
from app.core.controller_auth import controller_instance

from app.models.domain.source import Source
from app.core.database import SessionLocal

from app.config import SERVER_DOWNLOADER


class torrentController(object):
    def __init__(self, controller_instance):
        self.controller_instance = controller_instance
    def gen_token(self):
        return self.controller_instance.create_token('cli-web-torrent')
    def upload_torrent(self, file_path):
        payload = {'file': open(file_path, 'rb')}
        try:
            token = self.gen_token()
            if token:
                headers = {
                    'Authorization': f'Bearer {token}'
                }
                response = requests.post(f'{SERVER_DOWNLOADER}/torrent/upload-torrent', files=payload, headers=headers)
                if response.status_code == 200:
                    temp_source = Source.add(session=SessionLocal(), hash=response.json().get('hash', False), status="DOWNLOADING_TORRENT")
                    if temp_source:
                        return temp_source
        except Exception as err:
            print(f'torrentController.add_torrent exception - {err}')
        return False
    def check_hash(self, hash):
        try:
            token = self.gen_token()
            if token:
                headers = {
                    'Authorization': f'Bearer {token}'
                }
                response = requests.get(f'{SERVER_DOWNLOADER}/torrent/status/{hash}', headers=headers)
                if response.status_code == 200:
                    return response.json()
        except Exception as err:
            print(f'torrentController.check_hash exception - {err}')
        return False
    def list_files_by_hash(self, hash):
        try:
            token = self.gen_token()
            if token:
                headers = {
                    'Authorization': f'Bearer {token}'
                }
                response = requests.get(f'{SERVER_DOWNLOADER}/torrent/files/{hash}', headers=headers)
                if response.status_code == 200:
                    if len(response.json().get('files', []))>0:
                        return response.json().get('files', [])
        except Exception as err:
            print(f'torrentController.list_files_by_hash exception - {err}')
        return False


torrent_instance = torrentController(controller_instance=controller_instance)



def get_torrent_instance():
    return torrent_instance