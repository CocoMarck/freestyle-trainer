from jnius import autoclass, PythonJavaClass, java_method

MediaPlayer = autoclass("android.media.MediaPlayer")

class _PreparedListener(PythonJavaClass):
    __javainterfaces__ = ["android/media/MediaPlayer$OnPreparedListener"]

    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    @java_method("(Landroid/media/MediaPlayer;)V")
    def onPrepared(self, mp):
        self.owner._prepared = True
        if self.owner._autoplay:
            mp.start()
            self.owner._playing = True


class AndroidMediaPlayerAsync:
    def __init__(self, source, autoplay=False):
        self._media_player = None
        self._prepared = False
        self._playing = False
        self._autoplay = autoplay

        try:
            self._media_player = MediaPlayer()
            self._prepared_listener = _PreparedListener(self)
            self._media_player.setOnPreparedListener(self._prepared_listener)

            self._media_player.setDataSource(str(source))
            self._media_player.prepareAsync()

        except Exception as e:
            print("MediaPlayer init error:", e)
            if self._media_player:
                try:
                    self._media_player.release()
                except:
                    pass
            self._media_player = None

    def is_valid(self):
        return self._media_player is not None

    def play(self):
        if not self._prepared or not self._media_player:
            return False
        try:
            self._media_player.start()
            self._playing = True
            return True
        except Exception as e:
            print("ERROR:", e)
            return False

    def stop(self):
        if not self._prepared or not self._media_player:
            return False
        try:
            self._media_player.pause()
            self._media_player.seekTo(0)
            self._playing = False
            return True
        except Exception as e:
            print("ERROR:", e)
            return False

    def is_playing(self):
        if not self._media_player:
            return False
        try:
            return self._media_player.isPlaying()
        except Exception:
            return False

    def get_length(self):
        if not self._prepared or not self._media_player:
            return 0.0
        try:
            return self._media_player.getDuration() / 1000.0
        except Exception:
            return 0.0

    def get_position(self):
        if not self._prepared or not self._media_player:
            return 0.0
        try:
            return self._media_player.getCurrentPosition() / 1000.0
        except Exception:
            return 0.0

    def set_volume(self, volume):
        if not self._media_player:
            return False
        try:
            self._media_player.setVolume(volume, volume)
            return True
        except Exception as e:
            print("ERROR:", e)
            return False

    def release(self):
        if not self._media_player:
            return False
        try:
            self._media_player.release()
        except Exception:
            pass
        self._media_player = None
        self._prepared = False
        self._playing = False
        return True
