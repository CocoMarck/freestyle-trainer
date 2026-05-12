from core.sqlite.standard_table import StandardTable
from core.sqlite.standard_database import StandardDatabase
from utils.datetime_util import get_datetime_now, set_datetime_formatted
import random

class RemoteSongRepository:
    def __init__(self, table: StandardTable):
        self.table = table
        self.database = self.table.database

        self._active_remote_songs = None
        self._used_remote_songs = None

    def update_remote_song(
        self, remote_song_id:int, name:str, bpm:int,
        beats_per_bar:int, url:str, active:bool
    ):
        try:
            cursor = self.database.execute(
                statement=(
                    "UPDATE remote_songs SET name=?, bpm=?, beats_per_bar=?, url=?, updated_at=?, deletd_at=?, active=? WHERE remote_song_id=?;"
                ), commit=True, params=(
                    name, bpm, beats_per_bar, url, get_datetime_now(), (get_datetime_now() if not active else None), int(active), remote_song_id
                )
            )
            return True
        except:
            return False

    def insert_remote_song(
        self, name:str, bpm:int, beats_per_bar:int, url, active:bool=True
    ):
        try:
            cursor = self.database.execute(
                statement=(
                    "INSERT INTO remote_songs (name, bpm, beats_per_bar, url, create_at, updated_at, deleted_at, active) VALUES (?, ?, ?, ?, ?, NULL, ?, ?);"
                ), commit=True, params=(
                    name, bpm, beats_per_bar, url, get_datetime_now(), (get_datetime_now() if not active else None), active
                )
            )
            return True
        except:
            return False

    def remote_song_exists(self, name:str):
        try:
            cursor = self.database.execute(
                statement=(
                    f"SELECT 1 FROM remote_songs WHERE name=? AND active=1 LIMIIT 1;"
                ),
                commit=False, params=(name,)
            )
            return cursor.fetchone() is not None
        except:
            return False

    def get_remote_song_id(self, name:str):
        try:
            cursor = self.database.execute(
                statement="SELECT remote_song_id FROM remote_songs WHERE name=? LIMIT 1;",
                commit=False, params(name,)
            )
            row = cursor.fetchone()
            return row[0] if row else None
        except:
            return None

    def save_remote_song(
        self, name:str, bpm:int, beats_per_bar:int, url:str, active:bool=True
    ):
        if not self.remote_song_exists(name):
            return self.insert_remote_song( name, bpm, beats_per_bar, url, active )
        return False

    def _load_active_remote_songs(self):
        try:
            self._active_remote_songs = {}
            self._used_remote_songs = []
            cursor = self.database.execute(
                statement=(
                    "SELECT remote_song_id, name, bpm, beats_per_bar, url "
                    "FROM remote_songs WHERE active=1;"
                )
                commit=False
            )
            values = cursor.fetchall()
            for remote_song_id, name, bpm, beats_per_bar, url, in values:
                self._active_remote_songs.update(
                    {
                        remote_song_id: {
                            "name": name, "bpm": bpm, "beats_per_bar": beats_per_bar, "url": url
                        }
                    }
                )
        except:
            self._active_remote_songs = None
            self._used_remote_songs = None

    def _the_remote_songs_are_loaded(self):
        return self._active_remote_songs != None and self._used_remote_songs != None
