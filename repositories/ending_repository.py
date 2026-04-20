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
        self, ending_id:int, vocal_id:int, language_id:int, ending_text:str, active:bool
    ):
        ending_text = self.format_code(ending_text)
        try:
            cursor = self.database.execute(
                statement=(
                    f"UPDATE endings SET ending_text=?, updated_at=?, deleted_at=?, active=? WHERE ending_id=?;"
                ), commit=True, params=(
                    ending_text, get_datetime_now(), (get_datetime_now() if not active else None), int(active), ending_id
                )
            )
            return True
        except:
            return False
