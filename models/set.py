from .control_fields import ControlFields

class Set(ControlFields):
    def __init__(self):
        super().__init__()

        self.set_id: int=None
        self.set_name: str=None
        self.description: str=None
