from jnius import (
    autoclass,
    PythonJavaClass,
    java_method
)

MediaPlayer = autoclass("android.media.MediaPlayer")

# Preparar
class _PreparedListener(PythonJavaClass):
    __javainterfaces__ = [
        "android/media/MediaPlayer$OnPreparedListener"
    ]

    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    @java_method("(Landroid/media/MediaPlayer;)V")
    def onPrepared(self, mp):
        self.owner._prepared = True

        if self.owner._autoplay:
            mp.start()
            self.owner._playing = True


class _CompletionListener(PythonJavaClass):
    __javainterfaces__ = [
        "android/media/MediaPlayer$OnCompletionListener"
    ]

    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    @java_method("(Landroid/media/MediaPlayer;)V")
    def onCompletion(self, mp):
        self.owner._playing = False


class _ErrorListener(PythonJavaClass):
    __javainterfaces__ = [
        "android/media/MediaPlayer$OnErrorListener"
    ]

    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    @java_method("(Landroid/media/MediaPlayer;II)Z")
    def onError(self, mp, what, extra):
        self.owner._last_error = (what, extra)
        return True

# Media player
class AndroidMediaPlayerAsync:
    '''
    Media player async
    '''
    def __init__(self, source):

        self._prepared = False

        try:
            # Intentar obtener source con media player async
            self._media_player = MediaPlayer()

            self._prepared_listener = _PreparedListener(self)
            self._completion_listener = _CompletionListener(self)
            self._error_listener = _ErrorListener(self)

            self._media_player.setOnPreparedListener(
                self._prepared_listener
            )

            self._media_player.setOnCompletionListener(
                self._completion_listener
            )

            self._media_player.setOnErrorListener(
                self._error_listener
            )

            self._media_player.setDataSource( str(source) )
            self._media_player.prepareAsync()
        except Exception as e:
            # No se pudo cargar sound
            try:
                self._media_player.release()
            except Exception:
                pass

            self._media_player = None

    def get_position(self):
        if not self._prepared:
            return 0.0

        return (
            self._media_player.getCurrentPosition()
            / 1000.0
        )

    def play(self):
        if self._prepared:
            self._media_player.start()
            return True

        return False

    def stop(self):
        if not self._prepared:
            return False
        try:
            self._media_player.pause()
            self._media_player.seekTo(0)
            return True

        except Exception as e:
            print(e)
            return False


    def is_playing(self):
        if not self._media_player:
            return False

        try:
            return self._media_player.isPlaying()
        except Exception:
            return False

    def set_volume(self, volume):
        if not self._media_player:
            return False
        try:
            self._media_player.setVolume(volume, volume)
            return True
        except Exception as e:
            print("ERROR:", e)
            return False

    def get_length(self) -> bool:
        if not self._media_player:
            return 0.0
        if not self._prepared:
            return 0.0

        return self._media_player.getDuration() / 1000.0

    def release(self) -> bool:
        if self._media_player:
            try:
                self._media_player.release()
            except:
                pass

            self._media_player = None
            self._prepared = False

            return True

        return False

    def is_ready(self):
        return self._prepared

    # No se usan. Puede que no jalen porque no las uso. No han sido probadas.
    def pause(self) -> bool:
        if not self._media_player:
            return False
        try:
            self._media_player.pause()
            return True
        except Exception:
            return False

    def seek(self, seconds) -> bool:
        if not self._prepared:
            return False
        try:
            self._media_player.seekTo(
                int(seconds * 1000)
            )
            return True

        except Exception:
            return False
