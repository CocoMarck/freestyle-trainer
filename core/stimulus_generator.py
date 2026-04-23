import random

class StimulusGenerator:
    def __init__(self, word_repository=None, trigger_bars=4):
        self.word_repository = word_repository
        self.trigger_bars = trigger_bars
        self.bar_count = 0
        self._init_with_stimulus = True


    def update( self, signals ):
        if signals["reset_bar"] and (self.trigger_bars > 0):
            self.bar_count += 1
            if (self.bar_count == self.trigger_bars):
                self.bar_count = 0
                return self.word_repository.get_random_words( "es", limit=4 )
        if self._init_with_stimulus:
            self._init_with_stimulus = False
            return self.word_repository.get_random_words( "es", limit=4 )
        return None
