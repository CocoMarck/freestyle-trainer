from repositories.local_song_repository import LocalSongRepository
import random

class LocalSongController():
    def __init__(self, local_song_repository: LocalSongRepository):

        self.repository = local_song_repository

    def get_local_song(self, local_song_id):
        if not self.repository._the_local_songs_are_loaded():
            self.repository._load_active_local_songs()

        song_data = self.repository._active_local_songs[local_song_id]
        if not local_song_id in self.repository._used_local_songs:
            self.repository._used_local_songs.append( local_song_id )
        return song_data

    def get_random_local_song(self):
        if not self.repository._the_local_songs_are_loaded():
            self.repository._load_active_local_songs()

        not_used_local_song_ids = []
        for key_id in self.repository._active_local_songs.keys():
            if not (key_id in self.repository._used_local_songs):
                not_used_local_song_ids.append( key_id )
        if len(not_used_local_song_ids) == 0:
            self.repository._used_local_songs.clear()
            not_used_local_song_ids = list(self.repository._active_local_songs.keys())

        local_song_id = random.choice( not_used_local_song_ids )
        return self.get_local_song( local_song_id )
