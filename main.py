# DB `stimulus_generator_util`
from core.sqlite.standard_database import StandardDatabase
from core.sqlite.standard_table import StandardTable
from repositories.vocal_repository import VocalRepository
from repositories.language_repository import LanguageRepository
from repositories.ending_repository import EndingRepository
from repositories.word_repository import WordRepository
from repositories.local_song_repository import LocalSongRepository
from repositories.remote_song_repository import RemoteSongRepository

# Creación de db si no exite.
from config.paths import (
    DATA_DIR, SCHEMAS_STIMULUS_GENERATOR_FILES, LOCAL_SONG_FILES, REMOTE_SONG_FILES
)
from config.paths import (
    ANDROID_PATH
)
db = StandardDatabase( directory=DATA_DIR, name='stimulus_generator.sqlite' )
if not db.exists():
    print('Creando base de datos y aplicando schemas...')
    db.execute( 'PRAGMA foreign_keys = ON;', commit=True )
    tables = {
        "vocals": None,
        "languages": None,
        "endings": None,
        "words": None,
        "sets": None,
        "set_words": None,
        "local_songs": None,
        "remote_songs": None
    }
    for f in SCHEMAS_STIMULUS_GENERATOR_FILES:
        if f.name == "vocals.sql":
            tables["vocals"] = f

        elif f.name == "languages.sql":
            tables["languages"] = f

        elif f.name == "endings.sql":
            tables["endings"] = f

        elif f.name == "words.sql":
            tables["words"] = f

        elif f.name == "sets.sql":
            tables["sets"] = f

        elif f.name == "set_words.sql":
            tables["set_words"] = f

        elif f.name == "local_songs.sql":
            tables["local_songs"] = f

        elif f.name == "remote_songs.sql":
            tables["remote_songs"] = f

    for f in tables.values():
        db.init_schema( f )
vocals_table = StandardTable( db, "vocals" )
vocal_repository = VocalRepository( vocals_table )
vocal_repository.vocal_exists('a')

languages_table = StandardTable( db, 'languages' )
language_repository = LanguageRepository( languages_table )

endings_table = StandardTable( db, 'endings' )
ending_repository = EndingRepository( endings_table )

words_table = StandardTable( db, 'words' )
word_repository = WordRepository( words_table )

import json
default_values = None
default_words = None
with open("data/default_values.json", mode="r", encoding="utf-8") as read_file:
    default_values = json.load(read_file)
with open("data/default_words.json", mode="r", encoding="utf-8") as read_file:
    default_words = json.load(read_file)

for vocal in default_values['vocals']:
    save = vocal_repository.save_vocal( vocal_text=vocal )
    if save:
        print(vocal)
for language in default_values['languages']:
    save = language_repository.save_code( code=language )
    if save:
        print(language)
ending_id = 0
for code in default_values['endings'].keys():
    for vocal in default_values['endings'][code]:
        for ending in default_values['endings'][code][vocal]:
            ending_id += 1
            if not ending_repository.exists( ending_id ):
                print( ending_repository.insert_ending( vocal, code, ending, True ) )
            else:
                print( "Ya existe we: %s"%(ending_id,) )
for code in default_words.keys():
    for vocal_text in default_words[code].keys():
        dicts = default_words[code][vocal_text]
        for dict_word in dicts:
            ending_text = dict_word['ending']
            print("\n\n#", ending_text, vocal_text, code)
            for word_text in dict_word['words']:
                #print( ending_text, vocal_text, code, word_text )
                insert = word_repository.insert_word(
                    ending_text, vocal_text, code, word_text, active=True
                )
                if insert:
                    print(word_text)

local_songs_table = StandardTable( db, "local_songs" )
local_song_repository = LocalSongRepository( local_songs_table )
for f in LOCAL_SONG_FILES:
    json_song = None
    with open(f, mode="r", encoding="utf-8") as read_file:
        json_song = json.load(read_file)
    save = local_song_repository.save_local_song(
        json_song['name'], json_song['bpm'], json_song['beats_per_bar'], json_song['path']
    )
    if save:
        print( json_song['name'], json_song['bpm'], json_song['beats_per_bar'], json_song['path'] )

remote_songs_table = StandardTable( db, "remote_songs" )
remote_song_repository = RemoteSongRepository( remote_songs_table )
for f in REMOTE_SONG_FILES:
    json_song = None
    with open(f, mode="r", encoding="utf-8") as read_file:
        json_song = json.load(read_file)
    save = remote_song_repository.save_remote_song(
        json_song['name'], json_song['bpm'], json_song['beats_per_bar'], json_song['url']
    )
    if save:
        print( json_song['name'], json_song['bpm'], json_song['beats_per_bar'], json_song['url'] )
    

print('\n\n')
#input()

# SoundManager
from core.sound_manager_kivy import SoundManagerKivy
from core.sound_manager_android import SoundManagerAndroid
from core.sound_manager_android_async import SoundManagerAndroidAsync
sound_manager_kivy = SoundManagerKivy(volume=1.0)
sound_manager_android = SoundManagerAndroid(volume=1.0)
sound_manager_android_async = SoundManagerAndroidAsync(volume=1.0)

# Controller
from controllers.beat_controller import BeatController
from controllers.local_song_controller import LocalSongController
from controllers.remote_song_controller import RemoteSongController

local_song_controller = LocalSongController( local_song_repository, sound_manager_android )
beat_controller = BeatController( sound_manager_android )

remote_song_controller = RemoteSongController( remote_song_repository, sound_manager_android )

# Engine | Freestyle trainer
from core.dt_metronome import DTMetronome
from core.stimulus_generator import StimulusGenerator
from core.freestyle_trainer_engine import FreestyleTrainerEngine

metronome = DTMetronome( bpm=90, beats_per_bar=4, bpm_limit=200, beats_limit_per_bar=16 )
stimulus_generator = StimulusGenerator( word_repository=word_repository, ending_repository=ending_repository, trigger_bars=4 )

freestyle_trainer_engine = FreestyleTrainerEngine(
    metronome=metronome, stimulus_generator=stimulus_generator
)

# Kivy
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.metrics import dp
from kivy.app import App
from kivy.clock import Clock

# Android
from android import api_version

# App
from views.freestyle_trainer_screen import FreestyleTrainerScreen

# Construir aplicacion
vertical_padding_offsets = [0,0,0,0]
horizontal_padding_offsets = [0,0,0,0]
if api_version > 35:
    # Android 15 (API 35) y 16 son los que fuerzan el Edge-to-Edge
    # Standard de celus: `16:9`, `20:9`, `19:9`.
    vertical_padding_offsets=[0,0.05, 0,0.08]
    horizontal_padding_offsets=[0,0.05, 0.08,0]
#
screen = FreestyleTrainerScreen(
    engine=freestyle_trainer_engine, local_song_controller=local_song_controller,
    remote_song_controller=remote_song_controller, beat_controller=beat_controller,
    vertical_padding_offsets=vertical_padding_offsets,
    horizontal_padding_offsets=horizontal_padding_offsets
)
class FreestyleTrainerApp(App):
    def build(self):
        # Permisos
        from android.permissions import request_permissions, Permission
        request_permissions([
            #Permission.RECORD_AUDIO, # Para grabar sesiones, pero por ahora no.
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE
        ])

        # Init screen
        _screen = screen
        _screen.build()
        Clock.schedule_interval(_screen.update, 0.0)
        return _screen

    def on_pause(self):
        return True

    def on_resume(self):
        return True

if __name__ == '__main__':
    FreestyleTrainerApp().run()
