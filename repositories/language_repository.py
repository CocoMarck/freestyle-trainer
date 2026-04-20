from core.sqlite.standard_table import StandardTable
from core.sqlite.standard_database import StandardDatabase
from utils.datetime_util import get_datetime_now, set_datetime_formatted

class LanguageRepository:
    def __init__(
        self, table: StandardTable
    ):
        self.table = table
        self.database = self.table.database

    def format_code(self, text):
        return text.lower()

    def update_code(self, language_id:int, code:str, active:bool):
        code = self.format_code(code)
        try:
            cursor = self.database.execute(
                statement=(
                    f"UPDATE languages SET code=?, updated_at=?, deleted_at=?, active=? WHERE language_id=?;"
                ), commit=True, params=(
                    code, get_datetime_now(), (get_datetime_now() if not active else None), int(active), language_id
                )
            )
            return True
        except:
            return False

    def insert_code(self, code:str, active:bool=True):
        code = self.format_code(code)
        try:
            cursor = self.database.execute(
                statement=(
                    "INSERT INTO languages (code, created_at, updated_at, deleted_at, active) VALUES(?, ?, NULL, ?, ?);"
                ), commit = True, params=(
                    code, get_datetime_now(), (get_datetime_now() if not active else None), active
                )
            )
            return True
        except:
            return False

    def code_exists(self, code:str):
        try:
            cursor = self.database.execute(
                statement=(
                    f'SELECT 1 FROM languages WHERE code=? AND active=1 LIMIT 1;'
                ),
                commit=False, params=(code)
            )
            return cursor.fetchone() is not None
        except:
            return False

    def get_language_id(self, code):
        try:
            cursor = self.database.execute(
                statement="SELECT language_id FROM languages WHERE code=? LIMIT 1;",
                commit=False, params=(code,)
            )
            row = cursor.fetchone()
            return row[0] if row else None
        except:
            return None

    def save_code(self, code:str, active:bool=True):
        if not self.code_exists(code):
            return self.insert_code( code, active )
        return False

    def save(self, language_id:int=None, code:str=None, active:bool=True):
        updated = False
        inserted = False
        if language_id is not None:
            updated = self.update_code( language_id, code, active )
        if updated == False:
            inserted = self.insert_codel( code, active )
        return updated or inserted



