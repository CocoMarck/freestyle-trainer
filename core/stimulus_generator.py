from repositories.word_repository import WordRepository
from repositories.ending_repository import EndingRepository
import random

class StimulusGenerator:
    def __init__(self, word_repository:WordRepository, ending_repository:EndingRepository, trigger_bars=4):
        self.word_repository = word_repository
        self.ending_repository = ending_repository
        self.trigger_bars = trigger_bars
        self.bar_count = 1
        self._init_with_stimulus = True


    def reset_count( self ):
        self.bar_count = 1
        self._init_with_stimulus = True


    def update( self, signals ):
        stimulus_signals = {
            "init": self._init_with_stimulus,
            "bar_count": None,
            "count_bar": signals["reset_bar"] and (self.trigger_bars > 0),
            "get_stimulus": False,
            "stimulus": None,
            "ending_text": None
        }

        if stimulus_signals["count_bar"]:
            stimulus_signals["get_stimulus"] = (self.bar_count == self.trigger_bars)
            self.bar_count += 1
            if stimulus_signals["get_stimulus"]:
                self.bar_count = 1
                stimulus_signals["stimulus"] = self.word_repository.get_random_words( "es", limit=4 )

        if self._init_with_stimulus:
            self._init_with_stimulus = False
            stimulus_signals["stimulus"] = self.word_repository.get_random_words( "es", limit=4 )

        stimulus_signals["bar_count"] = self.bar_count

        if isinstance(stimulus_signals["stimulus"], tuple):
            ending_id, words = stimulus_signals["stimulus"]
            stimulus_signals["ending_text"] = self.ending_repository.get_ending_text(ending_id)

        return stimulus_signals
