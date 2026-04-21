from core.sqlite.standard_table import StandardTable
from core.sqlite.standard_database import StandardDatabase
from utils.datetime_util import get_datetime_now, set_datetime_formatted

class EndingRepository:
    def __init__(
        self, table: StandardTable
    ):
        self.table = table
        self.database = self.table.database

    def format_ending(self, text):
        return text.lower()

    def update_ending(
        self, ending_id:int, vocal_text:str, code:str, ending_text:str, active:bool
    ):
        ending_text = self.format_ending(ending_text)
        try:
            cursor = self.database.execute(
                statement=(
                    "UPDATE endings "
                    "SET vocal_id=(SELECT vocal_id FROM vocals WHERE vocal_text=?), "
                    "   language_id=(SELECT language_id FROM langauges WHERE code=?), "
                    "   ending_text=?, updated_at=?, deleted_at=? active=? "
                    "WHERE ending_id=?;"
                ), commit=True, params=(
                    vocal_text, code, ending_text, get_datetime_now(), (get_datetime_now() if not active else None), int(active), ending_id
                )
            )
            return True
        except:
            return False

    def insert_ending(
        self, vocal_text:str, code:str, ending_text:str, active:bool
    ):
        ending_text = self.format_ending(ending_text)
        try:
            cursor = self.database.execute(
                statement=(
                    "INSERT INTO endings (vocal_id, language_id, ending_text, created_at, updated_at, deleted_at, active)\n"
                    "SELECT v.vocal_id, l.language_id, ?, ?, NULL, ?, ?\n"
                    "FROM languages AS l\n"
                    "JOIN vocals AS v\n"
                    "WHERE v.vocal_text = ? AND l.code = ?;"
                ), commit = True, params=(
                    ending_text, get_datetime_now(), (get_datetime_now() if not active else None), int(active), vocal_text, code
                )
            )
            return True
        except:
            return False

    def exists(self, ending_id:int):
        try:
            cursor = self.database.execute(
                statement=(
                    f'SELECT 1 FROM endings WHERE ending_id=? LIMIT 1;'
                ),
                commit=False, params=(ending_id,)
            )
            return cursor.fetchone() is not None
        except:
            return False
