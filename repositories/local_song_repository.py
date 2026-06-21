from core.sqlite.standard_table import StandardTable
from core.sqlite.standard_database import StandardDatabase
from utils.datetime_util import get_datetime_now, set_datetime_formatted
import random

class LocalSongRepository:
    def __init__(
        self, table: StandardTable
    ):
        self.table = table
        self.database = self.table.database

        self._active_local_songs = None
        self._used_local_songs = None

    def update_local_song(self, local_song_id:int, name:str, bpm:int, beats_per_bar:int, path:str, active:bool):
        try:
            cursor = self.database.execute(
                statement=(
                    f"UPDATE local_songs SET name=?, bpm=?, beats_per_bar=?, path=?, updated_at=?, deleted_at=?, active=? WHERE local_song_id=?;"
                ), commit=True, params=(
                    name, bpm, beats_per_bar, path, get_datetime_now(), (get_datetime_now() if not active else None), int(active), local_song_id
                )
            )
            return True
        except:
            return False

    def insert_local_song(self, name:str, bpm:int, beats_per_bar:int, path:str, active:bool=True):
        try:
            cursor = self.database.execute(
                statement=(
                    "INSERT INTO local_songs (name, bpm, beats_per_bar, path, created_at, updated_at, deleted_at, active) VALUES(?, ?, ?, ?, ?, NULL, ?, ?);"
                ), commit = True, params=(
                    name, bpm, beats_per_bar, path, get_datetime_now(), (get_datetime_now() if not active else None), active
                )
            )
            return True
        except Exception as e:
            print(e)
            return False


    def local_song_exists(self, name:str):
        try:
            cursor = self.database.execute(
                statement=(
                    #'SELECT 1 FROM local_songs WHERE name=? AND active=1 LIMIT 1;'
                    'SELECT 1 FROM local_songs WHERE name=? LIMIT 1;'
                ),
                commit=False, params=(name,)
            )
            return cursor.fetchone() is not None
        except:
            return False

    def get_local_song_id(self, name:str):
        try:
            cursor = self.database.execute(
                statement="SELECT local_song_id FROM local_songs WHERE name=? LIMIT 1;",
                commit=False, params=(name,)
            )
            row = cursor.fetchone()
            return row[0] if row else None
        except:
            return None

    def save_local_song(
        self, name:str, bpm:int, beats_per_bar:int, path:str, active:bool=True
    ):
        song_id = self.get_local_song_id(name)
        if song_id is None:
            return self.insert_local_song( name, bpm, beats_per_bar, path, active )
        else:
            return self.update_local_song( song_id, name, bpm, beats_per_bar, path, active )

    def _song_dict(self, local_song_id, name, bpm, beats_per_bar, path, active ) -> dict:
        return {
            local_song_id: {
                "name":name, "bpm":bpm, "beats_per_bar":beats_per_bar,
                "path":path, "active": bool(active)
            }
        }


    def get_all_local_songs(self) -> dict:
        songs = {}
        cursor = self.database.execute(
            statement=(
                "SELECT local_song_id, name, bpm, beats_per_bar, path, active "
                "FROM local_songs"
            ),
            commit=False
        )
        values = cursor.fetchall()
        for local_song_id, name, bpm, beats_per_bar, path, active in values:
            songs.update(
                self._song_dict( local_song_id, name, bpm, beats_per_bar, path, active )
            )
        return songs

    def get_song(self, song_id:int) -> dict:
        cursor = self.database.execute(
            statement=(
                "SELECT local_song_id, name, bpm, beats_per_bar, path, active "
                "FROM local_songs WHERE local_song_id=? LIMIT 1;"
            ),
            commit=False, params=(song_id,)
        )
        value = cursor.fetchone()
        local_song_id, name, bpm, beats_per_bar, path, active = value
        return self._song_dict( local_song_id, name, bpm, beats_per_bar, path, active )


    def _load_active_local_songs(self):
        try:
            self._active_local_songs = {}
            self._used_local_songs = []
            cursor = self.database.execute(
                statement=(
                    "SELECT local_song_id, name, bpm, beats_per_bar, path, active "
                    "FROM local_songs "
                    "WHERE active=1;"
                ),
                commit=False
            )
            values = cursor.fetchall()
            for local_song_id, name, bpm, beats_per_bar, path, active in values:
                self._active_local_songs.update(
                    self._song_dict( local_song_id, name, bpm, beats_per_bar, path, active )
                )
        except:
            self._active_local_songs = None
            self._used_local_songs = None

    def _the_local_songs_are_loaded(self):
        return self._active_local_songs != None and self._used_local_songs != None

    def refresh_cache(self):
        self._load_active_local_songs()

    def get_all_local_song_names(self):
        try:
            cursor = self.database.execute(
                statement=(
                    "SELECT name FROM local_songs"
                ),
                commit=False
            )
            values = []
            for x in cursor.fetchall():
                values.append( x[0] )
            return values
        except:
            return []
