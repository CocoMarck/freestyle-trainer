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
class AndroidMediaPlayer:
    '''
    Media player async
    '''
    def __init__(self, source):

        self._prepared = False
        self._playing = False
        self._autoplay = False
        self._last_error = None

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

        self._media_player.setDataSource(source)

        # NO BLOQUEA
        self._media_player.prepareAsync()

    def get_position(self):
        if not self._prepared:
            return 0.0

        return (
            self._media_player.getCurrentPosition()
            / 1000.0
        )

    def seek(self, seconds):
        self._media_player.seekTo(
            int(seconds * 1000)
        )

    def play(self):
        if self._prepared:
            self._media_player.start()
            self._playing = True
            return True

        self._autoplay = True
        return False

    def stop(self):
        try:
            self._media_player.pause()
            self._media_player.seekTo(0)
            self._playing = False
            return True

        except Exception as e:
            print(e)
            return False

    def pause(self):
        try:
            self._media_player.pause()
            self._playing = False
            return True
        except Exception:
            return False

    def is_playing(self):
        if not self._media_player:
            return False

        try:
            return self._media_player.isPlaying()
        except Exception:
            return False

    def set_volume(self, volume):
        try:
            self._media_player.setVolume(volume, volume)
            return True
        except Exception as e:
            print("ERROR:", e)
            return False

    def get_length(self):
        if not self._prepared:
            return 0.0

        return self._media_player.getDuration() / 1000.0

    def release(self):
        if self._media_player:

            try:
                self._media_player.release()
            except:
                pass

            self._media_player = None

            self._prepared = False
            self._playing = False
            self._autoplay = False

            return True

        return False

    def is_ready(self):
        return self._prepared
