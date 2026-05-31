from .control_fields import ControlFields

class Vocal(ControlFields):
    def __init__(self):
        super().__init__()

        self.vocal_id: int=None
        self.vocal_text: str=None
