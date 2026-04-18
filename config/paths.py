from utils.resource_loader import ResourceLoader

resource_loader = ResourceLoader()

DATA_DIR = resource_loader.data_dir

SCHEMAS_DIR = resource_loader.base_dir.joinpath( 'schemas' )
SCHEMAS_STIMULUS_GENERATOR_DIR = SCHEMAS_DIR.joinpath( 'stimulus_generator' )
SCHEMAS_STIMULUS_GENERATOR_DIR_TREE = resource_loader.get_recursive_tree(
    SCHEMAS_STIMULUS_GENERATOR_DIR
)
SCHEMAS_STIMULUS_GENERATOR_FILES = SCHEMAS_STIMULUS_GENERATOR_DIR_TREE['file']
