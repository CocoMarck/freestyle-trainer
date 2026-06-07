from jnius import autoclass, PythonJavaClass, java_method

MediaPlayer = autoclass("android.media.MediaPlayer")

class _PreparedListener(PythonJavaClass):
    __javainterfaces__ = ["android/media/MediaPlayer$OnPreparedListener"]

    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    @java_method("(Landroid/media/MediaPlayer;)V")
    def onPrepared(self, mp):
        print(f"[DEBUG_MP] ¡OnPrepared disparado por Java para la rola: {self.owner.source}!")
        self.owner._prepared = True
        if self.owner._autoplay:
            print("[DEBUG_MP] Autoplay activo. Dando play...")
            mp.start()
            self.owner._playing = True
        else:
            print("[DEBUG_MP] Autoplay inactivo. Listo para reproducir manualmente.")


class AndroidMediaPlayerAsync:
    def __init__(self, source, autoplay=False):
        self.source = source  # Guardamos la ruta para los logs
        self._media_player = None
        self._prepared = False
        self._playing = False
        self._autoplay = autoplay

        print(f"\n[DEBUG_MP] Iniciando carga de: {self.source}")
        try:
            self._media_player = MediaPlayer()

            # CRUCIAL: Guardar la referencia exacta en el objeto para que Python no borre el listener
            self._prepared_listener = _PreparedListener(self)
            self._media_player.setOnPreparedListener(self._prepared_listener)

            print(f"[DEBUG_MP] Seteando data source...")
            self._media_player.setDataSource(str(source))

            print(f"[DEBUG_MP] Llamando a prepareAsync()... (No bloqueante)")
            self._media_player.prepareAsync()
            print(f"[DEBUG_MP] prepareAsync() lanzado con éxito.")

        except Exception as e:
            print("[DEBUG_MP] ERROR CRÍTICO EN INIT:", e)
            if self._media_player:
                try:
                    self._media_player.release()
                except:
                    pass
            self._media_player = None

    def is_valid(self):
        return self._media_player is not None

    def play(self):
        print(f"[DEBUG_MP] Intentando dar play... ¿Preparado?: {self._prepared}")
        if not self._prepared or not self._media_player:
            print("[DEBUG_MP] Play rechazado: El MediaPlayer aún no está preparado o es None.")
            return False
        try:
            self._media_player.start()
            self._playing = True
            print("[DEBUG_MP] play() ejecutado con éxito.")
            return True
        except Exception as e:
            print("[DEBUG_MP] ERROR EN PLAY:", e)
            return False

    def stop(self):
        print("[DEBUG_MP] Intentando detener/pausar...")
        if not self._prepared or not self._media_player:
            return False
        try:
            self._media_player.pause()
            self._media_player.seekTo(0)
            self._playing = False
            print("[DEBUG_MP] stop() ejecutado (pausa + seekTo(0)).")
            return True
        except Exception as e:
            print("[DEBUG_MP] ERROR EN STOP:", e)
            return False

    def is_playing(self):
        if not self._media_player:
            return False
        try:
            playing = self._media_player.isPlaying()
            # print(f"[DEBUG_MP] ¿isPlaying() en Java?: {playing}") # Opcional, puede saturar el log
            return playing
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
            print("[DEBUG_MP] ERROR EN SET_VOLUME:", e)
            return False

    def release(self):
        print(f"[DEBUG_MP] Liberando MediaPlayer para: {self.source}")
        if not self._media_player:
            return False
        try:
            self._media_player.release()
        except Exception as e:
            print("[DEBUG_MP] Error al liberar:", e)
        self._media_player = None
        self._prepared = False
        self._playing = False
        return True
