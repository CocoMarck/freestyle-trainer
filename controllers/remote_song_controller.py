from core.dt_metronome import DTMetronome
from core.sound_manager_vlc import SoundManagerVLC
from repositories.remote_song_repository import RemoteSongRepository
import random

class RemoteSongController():
    def __init__(
        self, remote_song_repository:RemoteSongRepository, sound_manager: SoundManagerVLC
    ):
        self.repository = remote_song_repository
        self.current_song = None
        self.sound_manager = sound_manager

    def get_song(self, song_id):
        if not self.repository._the_remote_songs_are_loaded():
            self.repository._load_active_remote_songs()
        
        song_data = self.repository._active_remote_songs[song_id]
        if not song_id in self.repository._used_remote_songs:
            self.repository._used_remote_songs.append( song_id )
        return song_data 
        
    def get_random_song(self):
        if not self.repository._the_remote_songs_are_loaded():
            self.repository._load_active_remote_songs()
        
        not_used_remote_song_ids = []
        for key_id in self.repository._active_remote_songs.keys():
            if not (key_id in self.repository._used_remote_songs):
                not_used_remote_song_ids.append( key_id )
        if len(not_used_remote_song_ids) == 0:
            self.repository._used_remote_songs.clear()
            not_used_remote_song_ids = list(self.repository._active_remote_songs.keys())
        
        remote_song_id = random.choice( not_used_remote_song_ids )
        return self.get_song( remote_song_id )
        
    def set_random_song(self):
        self.current_song = self.get_random_song()
        self.current_song.update ({
            "sound": self.sound_manager.get_sound( self.current_song['url'] )
        })
       
    def play_song(self):
        return self.sound_manager.play_sound( self.current_song['sound'] )
    
    def playing_song(self):
        if self.current_song:
            return self.sound_manager.is_sound_playing( self.current_song )

    def sync_song_with_metronome(self, metronome:DTMetronome):
        if self.current_song:
            metronome.set_and_reset_settings(
                self.current_song["bpm"], self.current_song["beats_per_bar"]
            )
            return True
