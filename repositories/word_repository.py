from core.sqlite.standard_table import StandardTable
from core.sqlite.standard_database import StandardDatabase
from utils.datetime_util import get_datetime_now, set_datetime_formatted

class WordRepository:
    def __init__( self, table: StandardTable ):
        self.table = table
        self.database = self.table.database


    def format_word(self, text):
        return text.lower()

    def update_word(
        self, word_id: int, ending_text, vocal_text, code, word_text, active:bool
    ):
        word_text = self.format_word(word_text)
        try:
            cursor = self.database.execute(
                statement=(
                    "UPDATE words "
                    "SET ending_id=( "
                    "   SELECT e.ending_id "
                    "   FROM endings e "
                    "   JOIN vocals v ON e.vocal_id=v.vocal_id "
                    "   JOIN languages l ON e.language_id=l.language_id "
                    "   WHERE e.ending_text=? AND v.vocal_text=? AND l.code=? "
                    "), "
                    "word_text=?, updated_at=?, deleted_at=? active=? "
                    "WHERE word_id=?;"
                ),
                commit=True, params=(
                    ending_text, vocal_text, code, word_text, get_datetime_now(), (get_datetime_now() if not active else None), int(active), word_id
                )
            )
            return True
        except:
            return False

    def insert_word(self, ending_text:str, vocal_text:str, code:str, word_text:str, active:bool):
        word_text = self.format_word(word_text)
        try:
            cursor = self.database.execute(
                statement=(
                    "INSERT INTO words (ending_id, word_text, created_at, updated_at, deleted_at, active) "
                    "SELECT e.ending_id, ?, ?, NULL, ?, ? "
                    "FROM endings e "
                    "JOIN vocals v ON e.vocal_id=v.vocal_id "
                    "JOIN languages l ON e.language_id=l.language_id "
                    "WHERE e.ending_text=? AND v.vocal_text=? AND l.code=?;"
                ),
                commit=True, params=(
                    word_text, get_datetime_now(), (get_datetime_now() if not active else None), int(active), ending_text, vocal_text, code
                )
            )
            return True
        except:
            return False

    def get_random_words(self, code="es", limit=1):
        words = []
        try:
            # Ending ID random
            cursor = self.database.execute(
                statement=(
                    "SELECT e.ending_id "
                    "FROM endings e "
                    "JOIN languages l ON e.language_id = l.language_id "
                    "WHERE e.active = 1 "
                    "   AND l.code = ? "
                    "ORDER BY RANDOM() "
                    "LIMIT 1;"
                ), commit=False, params=( code, )
            )
            ending_id = cursor.fetchone()[0]

            # Word random
            cursor = self.database.execute(
                statement=(
                    "SELECT w.word_text "
                    "FROM words w "
                    "JOIN endings e ON w.ending_id = e.ending_id "
                    "JOIN vocals v ON e.vocal_id = v.vocal_id "
                    "JOIN languages l ON e.language_id = l.language_id "
                    "WHERE w.active = 1 "
                    "   AND e.ending_id = ?"
                    "   AND l.code = ? "
                    "ORDER BY RANDOM() "
                    "LIMIT ?;"
                ), commit=False, params=( ending_id, code, limit )
            )
            words_fetchall = cursor.fetchall()
            for word in words_fetchall:
                words.append( word[0] )
            return words
        except:
            return words
