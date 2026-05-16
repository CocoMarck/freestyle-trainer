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

# Controller
from controllers.beat_controller import BeatController
from controllers.local_song_controller import LocalSongController
from controllers.remote_song_controller import RemoteSongController

# Screen
kv_string = None
with open('./views/freestyle_trainer_screen.txt', mode="r", encoding="utf-8") as read_file:
    kv_string = read_file.read()
Builder.load_string( kv_string )
class FreestyleTrainerScreen(Screen):
    def __init__(
        self,
        engine:FreestyleTrainerEngine, local_song_controller:LocalSongController,
        remote_song_controller:RemoteSongController,
        beat_controller:BeatController, vertical_padding_offsets=[0,0,0,0], horizontal_padding_offset=[0,0,0,0], **kwargs
    ):
        super().__init__(**kwargs)

        '''
        Widgets de string:
        self.main_vbox_layout
        self.label_bar_count
        self.label_last_stimulus
        '''

        self.engine = engine
        self.metronome = self.engine.metronome
        self.stimulus_generator = self.engine.stimulus_generator

        # Controller
        self.local_song_controller = local_song_controller
        self.remote_song_controller = remote_song_controller

        # Beat
        self.play_beat = False
        self.beat_controller = beat_controller

    def playing_sound(self):
        return (
            self.local_song_controller.playing_song() or self.remote_song_controller.playing_song()
        )

    def update(self, dt):
        if self.playing_sound():
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

            if self.play_beat:
                self.beat_controller.update( metronome_signals )
        else:
            '''
            Establece cancion. Configura y reinicia metronomo segun la song. Reincia conteo de compases de simulus generator.
            '''
            # Local
            #self.local_song_controller.set_random_song()
            #self.local_song_controller.play_song()
            #self.local_song_controller.sync_metronome_with_song( self.metronome )

            # Remote
            self.remote_song_controller.set_random_song()
            self.remote_song_controller.play_song()
            self.remote_song_controller.sync_metronome_with_song( self.metronome )

            # Stimulus
            self.stimulus_generator.reset_count()
