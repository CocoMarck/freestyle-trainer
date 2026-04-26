# Python
from functools import partial

# Kivy
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.properties import (
    ListProperty, NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.lang import Builder

# Freestyle trainer
from core.freestyle_trainer_engine import FreestyleTrainerEngine

# Screen
kv_string = None
with open('./views/freestyle_trainer_screen.txt', mode="r", encoding="utf-8") as read_file:
    kv_string = read_file.read()
Builder.load_string( kv_string )
class FreestyleTrainerScreen(Screen):
    def __init__(
        self, engine:FreestyleTrainerEngine=None, vertical_padding_offsets=[0,0,0,0], horizontal_padding_offset=[0,0,0,0], **kwargs
    ):
        super().__init__(**kwargs)

        '''
        Widgets de string:
        self.main_vbox_layout
        self.label_bar_count
        self.label_last_stimulus
        '''

        self.engine = engine

    def update(self, dt):
        engine_signals = self.engine.update(dt)
        metronome_signals = engine_signals['metronome']
        stimulus_signals = engine_signals['stimulus_generator']

        if metronome_signals['first_step_of_beat']:
            self.label_bar_count.text = (
                f"{metronome_signals['current_beat']} | {stimulus_signals['bar_count']}"
            )
            print( metronome_signals["current_beat"] )
        if stimulus_signals['init'] or stimulus_signals['get_stimulus']:
            self.label_last_stimulus.text = str( stimulus_signals["stimulus"] )
