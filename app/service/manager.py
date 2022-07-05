from threading import Thread
import time

from app.core.database import SessionLocal

from app.models.domain.source import Source
from app.models.domain.file import File

from app.core.torrent import get_torrent_instance



class manager(Thread):
    def __init__ (self):
        Thread.__init__(self)
    def check_torrent(self, data):
        temp_resp = get_torrent_instance().check_hash(hash=data.hash)
        if temp_resp:
            if temp_resp['size'] == temp_resp['downloaded']:
                Source.update_status(session=SessionLocal(), id=data.id, status="PENDING_ENCODE")
                torrent_files = get_torrent_instance().list_files_by_hash(hash=data.hash)
                if torrent_files:
                    for file in torrent_files:
                        File.add(session=SessionLocal(), source_id=data.id, name=file['name'], status="PENDING_ENCODING", serve_uri=file['serve'])

    def get_torrents(self):
        temp_data = Source.find_by_status(session=SessionLocal(), status="DOWNLOADING_TORRENT")
        if temp_data:
            for torrent in temp_data:
                self.check_torrent(data=torrent)
    def run(self):
        while True:
            self.get_torrents()
            time.sleep(10)

