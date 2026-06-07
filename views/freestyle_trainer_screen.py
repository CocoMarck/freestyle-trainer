# Python
from functools import partial

# Kivy
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.properties import (
    ListProperty, NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.lang import Builder

from kivy.graphics import Color, Rectangle

## Custom kviy widgets
from views.pykivy.widgets.metronome_circle import MetronomeCircle
from views.pykivy.widgets.screen_android_ready import ScreenAndroidReady
from views.pykivy.widgets.popup_grid_layout import PopupGridLayout
from views.pykivy.widgets.popup_standard_buttons import PopupStandardButtons
from views.pykivy.widgets.label_slider import LabelSlider

# Paths
from config.paths import KVSTRING_FILE

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

# Time
from utils.time_util import get_time

# Screen
kv_string = None
with open(KVSTRING_FILE, mode="r", encoding="utf-8") as read_file:
    kv_string = read_file.read()
Builder.load_string( kv_string )
class FreestyleTrainerScreen(ScreenAndroidReady):
    def __init__(
        self, *args, engine:FreestyleTrainerEngine, local_song_controller:LocalSongController,
        remote_song_controller:RemoteSongController,
        beat_controller:BeatController, **kwargs
    ):
        super().__init__(*args, **kwargs)

        '''
        Widgets de string:
        self.main_vbox_layout
        button_start
        button_stop
        button_settings
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
        self._update_length = False
        self._seconds_to_weit = 1
        self._count_weit = 0

        self.work = True

        # Song mode
        self._song_modes = ["acapella", "remote", "local"]
        self._current_song_mode = "acapella"

        # Padding
        self.bind(size=self._on_size)

        # Eventos de ventana
        Window.bind(on_minimize=self._on_minimize)
        Window.bind(on_restore=self._on_restore)

    def clear_song_information(self):
        self.label_current_song.text = ""
        self.label_active_ending_id.text = ""
        self.label_active_ending.text = ""

    # Loop work
    def stop_work(self):
        self.work = False
        # Restablecer data de metronomo y palabritas.
        self.metronome.reset_counts()
        self.stimulus_generator.reset_count()
        # Parar o no song
        if self.playing_sound( self.local_song_controller ):
            self.local_song_controller.stop_song()
        if self.playing_sound( self.remote_song_controller ):
            self.remote_song_controller.stop_song()
        # Limpiar mugrero
        self.clear_song_information()
        self.clear_stimulus_buttons()
        # Reset view
        self.build_metronome_circles()

    def start_work(self):
        self.work = True

    # Bind
    def _on_size(self, *args):
        return self.change_padding_using_resolution(self.main_vbox_layout)

    def _on_minimize(self, *args):
        self.stop_work()

    def _on_restore(self, *args):
        self.start_work()

    # Widgets wind
    def on_start(self, button):
        self.start_work()

    def on_stop(self, button):
        self.stop_work()

    def on_settings(self, button):
        popup = PopupGridLayout(
            title="Settings",
            cols=2, rows=5, row_default_height=self.height * 0.1,
            size_hint=(0.8, 0.8), text_ok='Ok'
        )

        # Metronome
        popup.second_container.add_widget(Label(text="BPM"))
        bpm_label_slider = LabelSlider(
            min=60, max=self.metronome.get_bpm_limit(), value=self.metronome.get_bpm(), step=10
        )
        popup.second_container.add_widget(bpm_label_slider)

        popup.second_container.add_widget(Label(text="Beats per bar"))
        bpb_label_slider = LabelSlider(
            min=2, max=self.metronome.get_beats_limit_per_bar(), value=self.metronome.get_beats_per_bar(), step=1
        )
        popup.second_container.add_widget(bpb_label_slider)

        popup.second_container.add_widget(Label(text="Play beat"))
        beat_toggle = ToggleButton(text="On", state='down' if self.play_beat else 'normal')
        popup.second_container.add_widget(beat_toggle)

        # Stimulus settings
        popup.second_container.add_widget(Label(text="Trigger bars"))
        tb_label_slider  = LabelSlider(
            min=1, max=8, value=self.stimulus_generator.trigger_bars, step=1
        )
        popup.second_container.add_widget(tb_label_slider)

        # Song options
        popup.second_container.add_widget(Label(text="Song mode"))
        spinner = Spinner(text=self._current_song_mode, values=self._song_modes)
        popup.second_container.add_widget(spinner)

        # Bind final
        popup.button_ok.bind(on_press=lambda i: self._apply_settings(
            bpm_label_slider.slider, bpb_label_slider.slider, tb_label_slider.slider, beat_toggle, spinner
        ))
        popup.open()

    def _apply_settings(self, bpm_slider, bpb_slider, tb_slider, beat_toggle, spinner):
        self.metronome.set_bpm(int(bpm_slider.value))
        self.metronome.set_beats_per_bar(int(bpb_slider.value))
        self.stimulus_generator.trigger_bars = (int(tb_slider.value))
        self.play_beat = beat_toggle.state == 'down'
        self._current_song_mode = spinner.text
        self.stop_work()
        self.start_work()

    # Build Widgets
    def build_metronome_circles(self):
        self._metronome_circles.clear()
        self.hbox_metronome.clear_widgets()
        for x in range( 0, self.metronome.get_beats_per_bar() ):
            circle = MetronomeCircle()
            self._metronome_circles.append( circle )
            self.hbox_metronome.add_widget(circle)

    # Build
    def build(self):
        self.button_start.bind( on_press=self.on_start )
        self.button_stop.bind( on_press=self.on_stop )
        self.button_settings.bind( on_press=self.on_settings )

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
            if isinstance(widget, Button):
                widget.background_normal = ""
                widget.background_color = rgba_to_normalized( color )

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
    def playing_sound(self, song_controller):
        return (
            song_controller.playing_song()
        )

    def song_loop(self, dt, song_controller):
        if self.playing_sound(song_controller):
            if self._update_length:
                self._count_weit += dt
                if self._count_weit >= self._seconds_to_weit:
                    self.label_length_value.text = str(
                        get_time(
                            song_controller.get_song_length(), "second", "minute"
                        )
                    )
                    self._update_length = False
                    self._count_weit = 0


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
            song_controller.set_random_song()
            song_controller.play_song()
            song_controller.sync_metronome_with_song( self.metronome )
            self.current_song_name = song_controller.get_song_name()

            self._update_length = True

            # Stimulus
            self.stimulus_generator.reset_count()

            # Texto
            self.label_bpm_value.text = str( self.metronome.get_bpm() )
            self.label_beats_per_bar.text = str( self.metronome.get_beats_per_bar() )

            # Metronome
            self.build_metronome_circles()

    def acapela_loop(self, dt):
        engine_signals = self.engine.update(dt)
        metronome_signals = engine_signals['metronome']
        stimulus_signals = engine_signals['stimulus_generator']

        if metronome_signals['first_step_of_beat']:
            self.label_bar_count.text = str( stimulus_signals['bar_count'] )
        if stimulus_signals['init'] or stimulus_signals['get_stimulus']:
            ending_id, words = stimulus_signals["stimulus"]
            self.label_current_song.text = "Acapela loop"
            self.label_active_ending_id.text = str( ending_id )
            self.label_active_ending.text = str( stimulus_signals['ending_text'] )
            self.label_bpm_value.text = str( self.metronome.get_bpm() )
            self.label_beats_per_bar.text = str( self.metronome.get_beats_per_bar() )
            self.clear_stimulus_buttons()
            self.add_stimulus_buttons(words)

        # Metronome play beat
        if self.play_beat:
            self.beat_controller.update( metronome_signals )

        # Color metronome
        self.coloring_metronome_circles( metronome_signals )

    def update(self, dt):
        if self.work:
            if self._current_song_mode == "acapella":
                self.acapela_loop(dt)
            elif self._current_song_mode == "remote":
                self.song_loop(dt, self.remote_song_controller)
            elif self._current_song_mode == "local":
                self.song_loop(dt, self.local_song_controller)


