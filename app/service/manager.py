from threading import Thread
import time
import requests

from app.core.database import SessionLocal

from app.models.domain.source import Source
from app.models.domain.file import File

from app.core.torrent import get_torrent_instance
from app.core.encoder import get_encoder_instance
from app.core.uploader import get_uploader_instance



class manager(Thread):
    def __init__ (self):
        Thread.__init__(self)
    def check_torrent(self, data):
        print(data.hash)
        temp_resp = get_torrent_instance().check_hash(hash=data.hash)
        print(temp_resp)
        if temp_resp:
            try:
                if temp_resp['size'] == temp_resp['downloaded']:
                    Source.update_status(session=SessionLocal(), id=data.id, status="PENDING_ENCODE")
                    torrent_files = get_torrent_instance().list_files_by_hash(hash=data.hash)
                    if torrent_files:
                        for file in torrent_files:
                            mime_type = self.check_mime_by_url(file['serve'])
                            if mime_type == 'video/x-matroska':
                                File.add(session=SessionLocal(), source_id=data.id, name=file['name'], status="PENDING_ENCODING", serve_uri=file['serve'])
            except Exception as err:
                print(f'manager.check_torrent exception - {err}')
    def check_mime_by_url(self, url):
        try:
            response = requests.head(url)
            if response.status_code == 200:
                return response.headers.get('content-type')
        except Exception as err:
            print(f'manager.check_mime_by_url exception - {err}')
        return False
    def deal_downloading_torrent(self):
        temp_data = Source.find_by_status(session=SessionLocal(), status="DOWNLOADING_TORRENT")
        if temp_data:
            for torrent in temp_data:
                self.check_torrent(data=torrent)
    def deal_send_encode(self):
        temp_data = File.find_by_status(session=SessionLocal(), status="PENDING_ENCODING")
        if temp_data:
            for file in temp_data:
                response_create_encode = get_encoder_instance().create_encode(source_id=file.source_id, serve_uri=file.serve_uri)
                if response_create_encode:
                    File.update_name_hash(session=SessionLocal(), id=file.id, name_hash=response_create_encode['name'])
                    File.update_status(session=SessionLocal(), id=file.id, status='PENDING_DOWNLOAD')
    def deal_encoding(self):
        temp_data = File.find_by_statuses(session=SessionLocal(), statuses=["PENDING_DOWNLOAD", "DOWNLOADING", "PENDING_ENCODE", "ENCODING", "DONE"])
        if temp_data:
            for item in temp_data:
                temp_data_encoding = get_encoder_instance().get_data_by_hash(hash=item.name_hash)
                if temp_data_encoding:
                    if item.status == "DONE":
                        File.update_serve(session=SessionLocal(), id=item.id, serve_uri=temp_data_encoding['serve'])
                    else:
                        print(temp_data_encoding)
                        print(item.name_hash)
                        if 'status' in temp_data_encoding:
                            File.update_status(session=SessionLocal(), id=item.id, status=temp_data_encoding['status'])
                            File.update_progress(session=SessionLocal(), id=item.id, progress=temp_data_encoding['progress'])
                        else:
                            print('dindt find file')
    def deal_upload(self):
        temp_data = File.find_by_statuses(session=SessionLocal(), statuses=['DONE'])
        if temp_data:
            for item in temp_data:
                temp_data_encoding = get_encoder_instance().get_data_by_hash(hash=item.name_hash)
                if temp_data_encoding:
                    try:
                        item_updated_content = File.update_serve(session=SessionLocal(), id=item.id, serve_uri=temp_data_encoding['serve'])
                        temp_response_upload = get_uploader_instance().upload(serve_uri=item_updated_content.serve_uri)
                        if temp_response_upload:
                            File.update_status(session=SessionLocal(), id=item.id, status='FINISH')
                            print(temp_response_upload)
                            File.update_serve(session=SessionLocal(), id=item.id, serve_uri=temp_response_upload['url'])
                    except Exception as err:
                        print(f'manager.deal_upload exception - {err}')
    def handle_finish_source(self):
        temp_data = Source.find_by_status(session=SessionLocal(), status='PENDING_ENCODE')
        if temp_data:
            for source in temp_data:
                temp_file = File.find_by_id_source(session=SessionLocal(), id_source=source.id)
                if temp_file:
                    has_break = False
                    for file in temp_file:
                        if file.status != 'FINISH':
                            has_break = True
                            break
                    if has_break == False:
                        Source.update_status(session=SessionLocal(), id=source.id, status='FINISH')
    def get_torrents(self):
        self.deal_downloading_torrent()
        self.deal_send_encode()
        self.deal_encoding()
        self.deal_upload()
        self.handle_finish_source()
    def run(self):
        while True:
            self.get_torrents()
            time.sleep(10)

