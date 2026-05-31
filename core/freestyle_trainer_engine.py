from core.dt_metronome import DTMetronome
from core.stimulus_generator import StimulusGenerator

class FreestyleTrainerEngine():
    def __init__(self, metronome: DTMetronome, stimulus_generator: StimulusGenerator):
        self.metronome = metronome
        self.stimulus_generator = stimulus_generator

        self._last_stimulus = None

    def update(self, dt):
        # Eventos
        metronome_signals = self.metronome.update(dt)

        stimulus_signals = self.stimulus_generator.update(metronome_signals)
        if isinstance(stimulus_signals["stimulus"], tuple):
            self._last_stimulus = stimulus_signals["stimulus"]

        return {
            "metronome": metronome_signals,
            "stimulus_generator": stimulus_signals
        }

    def get_last_stimulus(self):
        return self._last_stimulus
