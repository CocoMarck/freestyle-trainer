from jnius import autoclass, cast
from core.android_sound_info import get_audio_length

MediaPlayer = autoclass("android.media.MediaPlayer")
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Uri = autoclass('android.net.Uri')

class AndroidMediaPlayer:
    '''
    MediaPlayer nativo de Android. Deberia soportar url y rutas de archivo.
    '''
    def __init__(self, source):
        self._media_player = None
        self._source = source

        try:
            self._media_player = MediaPlayer()

            source_str = str(source)

            # Si es una URL de internet o streaming, se setea directo por texto
            if source_str.startswith("http://") or source_str.startswith("https://") or source_str.startswith("rtsp://"):
                self._media_player.setDataSource(source_str)
            else:
                # Es un archivo local o un Content URI del selector nativo.
                # Aplicamos el truco del FileDescriptor para saltar Scoped Storage.
                activity = PythonActivity.mActivity
                context = activity.getApplicationContext()
                content_resolver = context.getContentResolver()

                if source_str.startswith('content://'):
                    file_uri = Uri.parse(source_str)
                else:
                    # Si es una ruta absoluta limpia de Linux (/storage/emulated/0...)
                    File = autoclass('java.io.File')
                    file_uri = Uri.fromFile(File(source_str))

                # Abrimos el canal nativo como modo lectura ("r")
                pfd = content_resolver.openFileDescriptor(file_uri, "r")
                fd = pfd.getFileDescriptor()

                # Le alimentamos el descriptor directo a la instancia
                self._media_player.setDataSource(fd)
                pfd.close() # Se cierra el puente, MediaPlayer ya retiene el archivo en RAM nativa

            # Una vez asignado el origen, preparamos síncronamente
            self._media_player.prepare()

        except Exception as e:
            print("MediaPlayer init error:", e)
            if self._media_player:
                try:
                    self._media_player.release()
                except:
                    pass
            self._media_player = None

    def is_valid(self) -> bool:
        return self._media_player is not None

    def play(self) -> bool:
        if not self._media_player:
            return False

        try:
            self._media_player.start()
            return True

        except Exception as e:
            print("ERROR:", e)
            return False

    def stop(self) -> bool:
        if not self._media_player:
            return False

        try:
            self._media_player.pause()
            self._media_player.seekTo(0)
            return True

        except Exception as e:
            print("ERROR:", e)
            return False

    def is_playing(self) -> bool:
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

    def get_length(self) -> float:
        # SoundPool no trackea duraciones largas, usualmente es para samples cortos (< 5-10s)
        try:
            return get_audio_length(self.source)
        except Exception:
            return 0.0
        '''
        if not self._media_player:
            return 0.0
        try:
            return self._media_player.getDuration() / 1000.0
        except Exception:
            return 0.0
        '''

    def release(self):
        if not self._media_player:
            return False

        try:
            self._media_player.release()
        except Exception:
            pass

        self._media_player = None

        return True
    # Otros que no se usan aca. No testados. jejej
    def get_position(self):
        if not self._media_player:
            return 0.0

        try:
            return self._media_player.getCurrentPosition() / 1000.0
        except Exception:
            return 0.0

    def pause(self):
        if not self._media_player:
            return False

        try:
            self._media_player.pause()
            return True
        except Exception:
            return False

    def seek(self, seconds):
        if not self._media_player:
            return False

        try:
            self._media_player.seekTo(
                int(seconds * 1000)
            )
            return True
        except Exception:
            return False
