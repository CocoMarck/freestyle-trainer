from core.dt_metronome import DTMetronome
from entities.isound_manager import ISoundManager

class ISongController():
    def __init__(self, sound_manager: ISoundManager):
        self.sound_manager = sound_manager

    def get_song(self, song_id) -> object:
        pass

    def get_random_song(self) -> object:
        pass

    def set_random_song(self):
        pass

    def play_song(self):
        pass

    def get_song_name(self) -> str:
        pass

    def get_song_length(self) -> float:
        pass

    def playing_song(self) -> bool:
        pass

    def sync_metronome_with_song(self, metronome:DTMetronome) ->bool:
        pass
