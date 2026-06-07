from repositories.local_song_repository import LocalSongRepository
from core.dt_metronome import DTMetronome
from entities.isong_controller import ISongController
import random

class LocalSongController( ISongController ):
    def __init__(
        self, local_song_repository: LocalSongRepository, *kwargs
    ):
        super().__init__(*kwargs)
        self.repository = local_song_repository

        self.current_song = None

    def get_song(self, song_id):
        if not self.repository._the_local_songs_are_loaded():
            self.repository._load_active_local_songs()

        song_data = self.repository._active_local_songs[song_id]
        if not song_id in self.repository._used_local_songs:
            self.repository._used_local_songs.append( song_id )
        return song_data

    def get_random_song(self):
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
        return self.get_song( local_song_id )

    def set_random_song(self):
        self.current_song = self.get_random_song()
        self.current_song.update({
            "sound": self.sound_manager.get_sound( self.current_song['path'] )
        })

    def play_song(self):
        return self.sound_manager.play_sound( self.current_song['sound'] )

    def stop_song(self):
        return self.sound_manager.stop_sound( self.current_song['sound'] )

    def get_song_name(self):
        return self.current_song['name']

    def get_song_length(self):
        return self.sound_manager.get_sound_length( self.current_song['sound'] )

    def playing_song(self):
        if self.current_song:
            return self.sound_manager.is_sound_playing( self.current_song['sound'] )

    def sync_metronome_with_song(self, metronome:DTMetronome):
        if self.current_song:
            metronome.set_and_reset_settings(
                self.current_song["bpm"], self.current_song["beats_per_bar"]
            )
            return True
