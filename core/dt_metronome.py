
class DTMetronome():
    def __init__(
        self, bpm=120, beats_per_bar=4, bpm_limit=200, beats_limit_per_bar=16
    ):
        # Valores default
        self._INITIAL_BPM = bpm
        self._INITIAL_BEATS_PER_BAR = beats_per_bar
        self._INITIAL_BPM_LIMIT = bpm_limit
        self._INITIAL_BEATS_LIMIT_PER_BAR = beats_limit_per_bar

        # Valores usables
        self.bpm = self._INITIAL_BPM
        self.beats_per_bar = self._INITIAL_BEATS_PER_BAR

        self.bpm_limit = self._INITIAL_BPM_LIMIT
        self.beats_limit_per_bar = self._INITIAL_BEATS_LIMIT_PER_BAR

        self._current_beat = 1
        self._count_dt_of_beat = 0

        self.set_settings()

    def get_beat_interval(self):
        # Obtener duración de cada beat en segundos.
        return (60 / self.bpm)

    def get_beats_per_bar_interval(self):
        # Obtener duración de barra en segundos.
        return (self.get_beat_interval() * self.beats_per_bar)

    def get_current_beat(self):
        return self._current_beat

    def validate_and_set_bpm(self):
        '''
        Establece bpm a unos aceptables, no crash.
        '''
        if self.bpm <= 0:
            self.bpm = self._INITIAL_BPM
        if self.bpm_limit > 0:
            if self.bpm > self.bpm_limit:
                self.bpm = self.bpm_limit

    def validate_and_set_beats_per_bar(self):
        '''
        Esatablce beats a unos aceptables, no crash.
        '''
        if self.beats_per_bar < 1:
            self.beats_per_bar = 1
        if self.beats_limit_per_bar > 1:
            if self.beats_per_bar > self.beats_limit_per_bar:
                self.beats_per_bar = self.beats_limit_per_bar

    def set_settings(self):
        '''
        Establecer configuración del metronomo
        '''
        self.validate_and_set_bpm()
        self.validate_and_set_beats_per_bar()


    def determine_current_beat(self, dt):
        change_beat = self._count_dt_of_beat >= self.get_beat_interval()

        if change_beat:
            self._count_dt_of_beat = 0
            self._current_beat += 1
        first_step_of_beat = self._count_dt_of_beat == 0

        # Delta time actual analizado
        real_count_dt_of_beat = self._count_dt_of_beat

        # Compas
        reset_bar = self._current_beat == self.beats_per_bar+1
        if reset_bar:
            self._current_beat = 1
            self._count_dt_of_beat = 0 # Esto no se deberia necesitar. Pero sepa la bola... Doble verificación.

        # En que tempo va
        is_first_beat, is_last_beat, is_another_beat = False, False, False
        if first_step_of_beat:
            is_first_beat = self._current_beat == 1
            is_last_beat = self._current_beat == self.beats_per_bar
            is_another_beat = (not is_another_beat) and (not is_last_beat)

        # Paso antes de la barra
        step_before_the_bar = (
            (self._current_beat == self.beats_per_bar) and
            (real_count_dt_of_beat >= self.get_beat_interval())
        )

        # Sumar dt
        self._count_dt_of_beat += dt

        return {
            "change_beat": change_beat,
            "first_step_of_beat": first_step_of_beat,
            "reset_bar": reset_bar,
            "is_first_beat": is_first_beat,
            "is_last_beat": is_last_beat,
            "is_another_beat": is_another_beat,
            "step_before_the_bar": step_before_the_bar,
            "current_beat": self._current_beat,
            "count_dt": real_count_dt_of_beat
        }


    def update(self, dt):
        '''
        Chamba principal
        '''
        signals = self.determine_current_beat(dt)

        return signals

