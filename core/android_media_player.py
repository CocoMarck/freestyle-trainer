from jnius import autoclass

MediaPlayer = autoclass("android.media.MediaPlayer")

class AndroidMediaPlayer:
    '''
    MediaPlayer nativo de Android. Deberia soportar url y rutas de archivo.
    '''
    def __init__(self, source):
        self._media_player = MediaPlayer()
        self._media_player.setDataSource(source)
        self._media_player.prepare()

    def play(self):
        try:
            self._media_player.start()
            return True
        except Exception as e:
            print("ERROR:", e)
            return False

    def stop(self):
        try:
            self._media_player.pause()
            self._media_player.seekTo(0)
            return True
        except Exception as e:
            print("ERROR:", e)
            return False

    def is_playing(self):
        return self._media_player.isPlaying()

    def set_volume(self, volume):
        try:
            self._media_player.setVolume(volume, volume)
            return True
        except Exception as e:
            print("ERROR:", e)
            return False

    def get_length(self):
        return self._media_player.getDuration() / 1000.0

    def release(self):
        if self._media_player:
            self._media_player.release()
            self._media_player = None
            return True
        return False
