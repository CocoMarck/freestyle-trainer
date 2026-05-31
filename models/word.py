from .control_fields import ControlFields

class Word(ControlFields):
    def __init__(self):
        super().__init__()

        self.word_id: int=None
        self.word_text: str=None
        self.ending_id: int=None
