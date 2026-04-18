from .control_fields import ControlFields

class Ending(ControlFields):
    def __init__(self):
        super().__init__()

        self.ending_id: int=None
        self.ending_text: str=None
        self.vocal_id: int=None
        self.language_id: int=None
