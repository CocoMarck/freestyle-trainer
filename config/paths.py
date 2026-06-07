from utils.resource_loader import ResourceLoader

resource_loader = ResourceLoader()

DATA_DIR = resource_loader.data_dir

SCHEMAS_DIR = resource_loader.base_dir.joinpath( 'schemas' )
SCHEMAS_STIMULUS_GENERATOR_DIR = SCHEMAS_DIR.joinpath( 'stimulus_generator' )
SCHEMAS_STIMULUS_GENERATOR_DIR_TREE = resource_loader.get_recursive_tree(
    SCHEMAS_STIMULUS_GENERATOR_DIR
)
SCHEMAS_STIMULUS_GENERATOR_FILES = SCHEMAS_STIMULUS_GENERATOR_DIR_TREE['file']
LOCAL_SONGS_DIR = DATA_DIR.joinpath('songs', 'local')
REMOTE_SONGS_DIR = DATA_DIR.joinpath('songs', 'remote')

LOCAL_SONGS_DIR_TREE = resource_loader.get_recursive_tree( LOCAL_SONGS_DIR )
LOCAL_SONG_FILES = LOCAL_SONGS_DIR_TREE['file']

REMOTE_SONGS_DIR_TREE = resource_loader.get_recursive_tree( REMOTE_SONGS_DIR )
REMOTE_SONG_FILES = REMOTE_SONGS_DIR_TREE['file']

VIEWS_DIR = resource_loader.base_dir.joinpath( 'views' )
KVSTRING_FILE = VIEWS_DIR.joinpath('freestyle_trainer_screen.txt')

TEMP_DIR = resource_loader.base_dir.joinpath('tmp')
AUDIO_DIR = resource_loader.resources_dir.joinpath( 'audio' )
TEMPO_DIR = AUDIO_DIR.joinpath( 'tempo' )
DICT_TEMPO_DIR = resource_loader.get_recursive_tree( TEMPO_DIR )
TEMPO_FILES = sorted( DICT_TEMPO_DIR["file"] )
