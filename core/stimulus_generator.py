import random

class StimulusGenerator:
    def __init__(self, db=None, trigger_bars=4):
        self.db = db
        self.trigger_bars = trigger_bars
        self.bar_count = 0
        self._init_with_stimulus = True


    def update( self, signals ):
        if signals["reset_bar"] and (self.trigger_bars > 0):
            self.bar_count += 1
            if (self.bar_count == self.trigger_bars):
                self.bar_count = 0
                return random.choice( ["texto", "palabra", "coca", "chido"] )
        if self._init_with_stimulus:
            self._init_with_stimulus = False
            return random.choice( ["texto", "palabra", "coca", "chido"] )
        return None
