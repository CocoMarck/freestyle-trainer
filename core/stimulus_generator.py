import random

class StimulusGenerator:
    def __init__(self, word_repository=None, trigger_bars=4):
        self.word_repository = word_repository
        self.trigger_bars = trigger_bars
        self.bar_count = 0
        self._init_with_stimulus = True


    def update( self, signals ):
        stimulus_signals = {
            "init": self._init_with_stimulus,
            "bar_count": None,
            "count_bar": signals["reset_bar"] and (self.trigger_bars > 0),
            "get_stimulus": False,
            "stimulus": None
        }

        if stimulus_signals["count_bar"]:
            self.bar_count += 1
            stimulus_signals["get_stimulus"] = (self.bar_count == self.trigger_bars)
            if stimulus_signals["get_stimulus"]:
                self.bar_count = 0
                stimulus_signals["stimulus"] = self.word_repository.get_random_words( "es", limit=4 )

        if self._init_with_stimulus:
            self._init_with_stimulus = False
            stimulus_signals["stimulus"] = self.word_repository.get_random_words( "es", limit=4 )

        stimulus_signals["bar_count"] = self.bar_count

        return stimulus_signals
