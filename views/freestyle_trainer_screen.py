# Python
from functools import partial

# Kivy
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.properties import (
    ListProperty, NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.lang import Builder

from kivy.graphics import Color, Rectangle

# Freestyle trainer
from core.freestyle_trainer_engine import FreestyleTrainerEngine

# Controller
from controllers.beat_controller import BeatController
from controllers.local_song_controller import LocalSongController
from controllers.remote_song_controller import RemoteSongController

# Colors
from utils.colors import (
    get_rgba, invert_rgb, invert_rgba, rgba_to_normalized, scale_rgba, random_rgba, is_the_rgba_color_bright
)

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

    # Freestyle
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
                ending_id, words = stimulus_signals["stimulus"]
                words_text = (
                    f"ending_id: {ending_id}\n"
                    f"{stimulus_signals['ending_text']}\n"
                    "------------\n"
                )
                for word in words:
                    words_text += f"{word}\n"
                self.label_last_stimulus.text = words_text[:-1]

                # Cambiar color
                self.set_random_colors()

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


    # GUI
    def set_random_colors(self):
        # Obtener colores aleatoreos
        color = random_rgba()
        invert_color = invert_rgba( color )

        # Crear o mudificar rect y pintar en base a este.
        if not hasattr(self, "rect_window"):
            with self.canvas.before:
                self.color_window = Color( *rgba_to_normalized( color ) )
                self.rect_window = Rectangle(pos=self.pos, size=self.size)
            self.bind(
                pos=lambda inst, val: setattr(self.rect_window, 'pos', inst.pos),
                size=lambda inst, val: setattr(self.rect_window, 'size', inst.size)
            )
        else:
            self.color_window.rgba = rgba_to_normalized( color )
            self.rect_window.pos=self.pos
            self.rect_window.size=self.size

        # Pintar widgets
        for widget in self.walk():
            if isinstance(widget, Label):
                widget.color = rgba_to_normalized( invert_color )
