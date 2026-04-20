from core.sqlite.standard_table import StandardTable
from core.sqlite.standard_database import StandardDatabase
from utils.datetime_util import get_datetime_now, set_datetime_formatted

class VocalRepository:
    def __init__(
        self, table: StandardTable
    ):
        self.table = table
        self.database = self.table.database

    def format_vocal(self, text):
        return text.lower().replace(' ', '')

    def update_vocal(self, vocal_id:int, vocal_text:str, active:bool):
        vocal_text = self.format_vocal(vocal_text)
        try:
            cursor = self.database.execute(
                statement=(
                    f"UPDATE vocals SET vocal_text=?, updated_at=?, deleted_at=?, active=? WHERE vocal_id=?;"
                ), commit=True, params=(
                    vocal_text, get_datetime_now(), (get_datetime_now() if not active else None), int(active), language_id
                )
            )
            return True
        except:
            return False

    def insert_vocal(self, vocal_text:str, active:bool=True):
        vocal_text = self.format_vocal(vocal_text)
        try:
            cursor = self.database.execute(
                statement=(
                    "INSERT INTO vocals (vocal_text, created_at, updated_at, deleted_at, active) VALUES(?, ?, NULL, ?, ?);"
                ), commit = True, params=(
                    vocal_text, get_datetime_now(), (get_datetime_now() if not active else None), active
                )
            )
            return True
        except:
            return False

    def vocal_exists(self, vocal_text:str):
        try:
            cursor = self.database.execute(
                statement=(
                    f'SELECT 1 FROM vocals WHERE vocal_text=? AND active=1 LIMIT 1;'
                ),
                commit=False, params=(vocal_text)
            )
            return cursor.fetchone() is not None
        except:
            return False

    def get_vocal_id(self, vocal_text):
        try:
            cursor = self.database.execute(
                statement="SELECT vocal_id FROM vocals WHERE vocal_text=? LIMIT 1;",
                commit=False, params=(vocal_text,)
            )
            row = cursor.fetchone()
            return row[0] if row else None
        except:
            return None

    def save_vocal(self, vocal_text:str, active:bool=True):
        if not self.vocal_exists(vocal_text):
            return self.insert_vocal( vocal_text, active )
        return False

    def save(self, vocal_id:int=None, vocal_text:str=None, active:bool=True):
        updated = False
        inserted = False
        if vocal_id is not None:
            updated = self.update_vocal( vocal_id, vocal_text, active )
        if updated == False:
            inserted = self.insert_vocal( vocal_text, active )
        return updated or inserted


