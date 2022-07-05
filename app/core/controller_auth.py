import requests
from app.config import(
    SERVER_AUTH,
    SERVER_USERNAME,
    SERVER_PASSWORD,
    SERVER_DOWNLOADER,
    SERVER_ENCODER,
    SERVER_UPLOADER
)


class controller(object):
    def create_token(self, client_id):
        try:
            payload = {
                'username': SERVER_USERNAME,
                'password': SERVER_PASSWORD,
                'client_id': client_id
            }
            response = requests.post(f'{SERVER_AUTH}/auth/token', data=payload, timeout=10)
            if response.status_code == 200:
                return response.json().get('access_token', False)
        except Exception as err:
            print(f'controller.create_token exception - {err}')
        return False



controller_instance = controller()