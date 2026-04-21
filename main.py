# DB `stimulus_generator_util`
from core.sqlite.standard_database import StandardDatabase
from core.sqlite.standard_table import StandardTable
from repositories.vocal_repository import VocalRepository
from repositories.language_repository import LanguageRepository
from repositories.ending_repository import EndingRepository

# Creación de db si no exite.
from config.paths import DATA_DIR, SCHEMAS_STIMULUS_GENERATOR_FILES
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
        "set_words": None
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

    for f in tables.values():
        db.init_schema( f )
vocals_table = StandardTable( db, "vocals" )
vocal_repository = VocalRepository( vocals_table )
vocal_repository.vocal_exists('a')

languages_table = StandardTable( db, 'languages' )
language_repository = LanguageRepository( languages_table )

endings_table = StandardTable( db, 'endings' )
ending_repository = EndingRepository( endings_table )

import json
default_values = None
with open("data/default_values.json", mode="r", encoding="utf-8") as read_file:
    default_values = json.load(read_file)
for vocal in default_values['vocals']:
    print( vocal_repository.save_vocal( vocal_text=vocal ) )
for language in default_values['languages']:
    print( language_repository.save_code( code=language ) )
ending_id = 0
for code in default_values['endings'].keys():
    for vocal in default_values['endings'][code]:
        for ending in default_values['endings'][code][vocal]:
            ending_id += 1
            if not ending_repository.exists( ending_id ):
                print( ending_repository.insert_ending( vocal, code, ending, True ) )
            else:
                print( "Ya existe we: %s"%(ending_id,) )
#input()


# App
from core.dt_metronome import DTMetronome
from core.stimulus_generator import StimulusGenerator

metronome = DTMetronome( bpm=90, beats_per_bar=4, bpm_limit=200, beats_limit_per_bar=16 )
stimulus_generator = StimulusGenerator()

# Loop
import time

prev_time = time.perf_counter()
current_stimulus = None

while True:
    # Calcular delta time
    now = time.perf_counter()
    dt = now - prev_time
    prev_time = now

    # Eventos
    signals = metronome.update(dt)

    stimulus = stimulus_generator.update(signals)
    if isinstance(stimulus, str):
        current_stimulus = stimulus

    if signals['first_step_of_beat']:
        info = (
            f'current beat: {signals["current_beat"]}\n'
            f'reset bar: {signals["reset_bar"]}\n'
            f'first_step_of_beat: {signals["first_step_of_beat"]}\n'
            f'step_before_the_bar: {signals["step_before_the_bar"]}\n'
            "\n-------------\n"
        )
        print(info)
        stimulus_info = (
            f"StimulusGenerator\n"
            f"bar count: {stimulus_generator.bar_count}\n"
            f"{current_stimulus}\n"
            "\n-------------\n"
        )
        print(stimulus_info)

