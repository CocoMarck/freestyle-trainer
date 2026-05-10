from core.dt_metronome import DTMetronome
from core.sound_manager_vlc import SoundManagerVLC
import random

class RemoteSongController():
    def __init__(
        self, remote_song_repository=None, sound_manager: SoundManagerVLC=None
    ):
        self.repository = remote_song_repository
        self.current_song = None
        self.sound_manager = sound_manager
        
        self._audio_urls = [
            "https://cdn.pixabay.com/download/audio/2025/06/13/audio_0308f9186a.mp3?filename=onesevenbeatxs-slow-westcoast-boombap-type-beat-359448.mp3",
            "https://cdn.pixabay.com/download/audio/2025/05/10/audio_14aff3f684.mp3?filename=onesevenbeatxs-funny-boombap-reggae-old-school-rap-beat-prod-by-onesevenbeatxs-339287.mp3",
            "https://cdn.pixabay.com/download/audio/2023/10/28/audio_b4344b5177.mp3?filename=neigtheven-bpm-90-anubis-beat-by-neigtheven-173658.mp3",
            "https://cdn.pixabay.com/download/audio/2025/03/12/audio_6c9d36f509.mp3?filename=zharovbeatz-melodic-type-beat-dark-type-beat-rap-trap-beat-instrumental-312497.mp3",
            "https://cdn.pixabay.com/download/audio/2026/02/24/audio_5bd9d7e09b.mp3?filename=vaitsez-rap-rap-beat-beats-music-486586.mp3",
            "https://cdn.pixabay.com/download/audio/2024/03/09/audio_2126849754.mp3?filename=5xbeatz-90-s-old-school-type-beat-rap-instrumental-sample-me-2024-195157.mp3",
            "https://cdn.pixabay.com/download/audio/2026/02/03/audio_2a668968ec.mp3?filename=watermelon_beats-revenge-guitar-rap-beat-beats-music-2026-478872.mp3",
            "https://cdn.pixabay.com/download/audio/2026/01/24/audio_93f6604643.mp3?filename=watermelon_beats-rap-rap-beat-beats-music-violin-2026-472843.mp3"
        ]
        self._used_audio_url_ids = []

    def get_song(self, song_id):
        self._used_audio_url_ids.append( song_id )
        return self._audio_urls[song_id]
        
    def get_random_song(self):
        not_used_audio_url_ids = []
        ids = range(0, len(self._audio_urls))
        for i in ids:
            if not (i in ids):
                not_used_audio_url_ids.append( i )
        if len(not_used_audio_url_ids) == 0:
            self._used_audio_url_ids.clear()
            not_used_audio_url_ids = ids

        used_song_id = random.choice( not_used_audio_url_ids )
        return self.get_song(used_song_id)
        
    def set_random_song(self):
        self.current_song = self.sound_manager.get_sound( self.get_random_song() )
       
    def play_song(self):
        return self.sound_manager.play_sound( self.current_song )
    
    def playing_song(self):
        if self.current_song:
            return self.sound_manager.is_sound_playing( self.current_song )

    def sync_song_with_metronome(self, metronome:DTMetronome):
        if self.current_song:
            metronome.set_beats_per_bar( 4 )
            metronome.set_bpm( 90 )
            return True
