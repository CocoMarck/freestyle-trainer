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

## Custom kviy widgets
from views.pykivy.widgets.metronome_circle import MetronomeCircle
from views.pykivy.widgets.screen_android_ready import ScreenAndroidReady

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
class FreestyleTrainerScreen(ScreenAndroidReady):
    def __init__(
        self, *args, engine:FreestyleTrainerEngine, local_song_controller:LocalSongController,
        remote_song_controller:RemoteSongController,
        beat_controller:BeatController, vertical_padding_offsets=[0,0,0,0], horizontal_padding_offset=[0,0,0,0], **kwargs
    ):
        super().__init__(*args, **kwargs)

        '''
        Widgets de string:
        self.main_vbox_layout
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

        # Current song
        self.current_song_name = None

        # Metronome view
        self._metronome_circles = []
        self.build_metronome_circles()

        # Padding
        self.bind(size=self._on_size)

    # Bind
    def _on_size(self, *args):
        return self.change_padding_using_resolution(self.main_vbox_layout)

    # Build Widgets
    def build_metronome_circles(self):
        self._metronome_circles.clear()
        self.hbox_metronome.clear_widgets()
        for x in range( 0, self.metronome.get_beats_per_bar() ):
            circle = MetronomeCircle()
            self._metronome_circles.append( circle )
            self.hbox_metronome.add_widget(circle)

    # GUI Colorear
    def coloring_metronome_circles(self, metronome_signals):
        '''
        Metronomo | Visual
        '''
        for i in range( 0, len(self._metronome_circles) ):
            if metronome_signals['current_beat'] != i+1:
                self._metronome_circles[i].color.rgb = (1.0,1.0,1.0)

        if ( metronome_signals['current_beat']-1 in range( 0, len(self._metronome_circles) ) ):
            self._metronome_circles[ metronome_signals['current_beat']-1 ].color.rgb = (1.0,0.0,0.0)

    def set_random_colors(self):
        # Obtener colores aleatoreos
        color = random_rgba()
        invert_color = invert_rgba( color )
        if is_the_rgba_color_bright( color ):
            invert_color = scale_rgba(invert_color, 0.25)
        else:
            invert_color = scale_rgba(invert_color, 1.75)

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

    # Texto
    def format_word(self, text):
        new_text = ""
        count = 0
        for c in text.lower():
            if count <= 0:
                new_text += c.upper()
                count += 1
            else:
                new_text += c

        return new_text

    # Widgets
    def add_stimulus_buttons(self, stimulus):
        for text in stimulus:
            button = Button(
                text=self.format_word(text), size_hint=(1.0, 0.4), pos_hint={"x": 0.0, "y": 0.9}
            )
            self.hbox_last_stimulus.add_widget(button)

    def clear_stimulus_buttons(self):
        self.hbox_last_stimulus.clear_widgets()

    # Freestyle
    def playing_sound(self):
        return (
            self.local_song_controller.playing_song() or self.remote_song_controller.playing_song()
        )

    def update(self, dt):
        if self.playing_sound():
            # Freestyle
            engine_signals = self.engine.update(dt)
            metronome_signals = engine_signals['metronome']
            stimulus_signals = engine_signals['stimulus_generator']

            if metronome_signals['first_step_of_beat']:
                self.label_bar_count.text = str( stimulus_signals['bar_count'] )
            if stimulus_signals['init'] or stimulus_signals['get_stimulus']:
                ending_id, words = stimulus_signals["stimulus"]
                self.label_current_song.text = str( self.current_song_name )
                self.label_active_ending_id.text = str( ending_id )
                self.label_active_ending.text = str( stimulus_signals['ending_text'] )

                self.clear_stimulus_buttons()
                self.add_stimulus_buttons(words)

                # Cambiar color
                #self.set_random_colors()

            if self.play_beat:
                self.beat_controller.update( metronome_signals )

            # Color metronome
            self.coloring_metronome_circles( metronome_signals )
        else:
            '''
            Freestyle
            Establece cancion. Configura y reinicia metronomo segun la song. Reincia conteo de compases de simulus generator.
            '''
            # Local
            # self.local_song_controller.set_random_song()
            # self.local_song_controller.play_song()
            # self.local_song_controller.sync_metronome_with_song( self.metronome )
            # self.current_song_name = self.local_song_controller.current_song['name']

            # Remote
            self.remote_song_controller.set_random_song()
            self.remote_song_controller.play_song()
            self.remote_song_controller.sync_metronome_with_song( self.metronome )
            self.current_song_name = self.remote_song_controller.current_song['name']

            # Stimulus
            self.stimulus_generator.reset_count()

            # Texto
            self.label_bpm_value.text = str( self.metronome.get_bpm() )
            self.label_beats_per_bar.text = str( self.metronome.get_beats_per_bar() )

            # Metronome
            self.build_metronome_circles()
