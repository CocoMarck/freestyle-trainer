# Android configs
import pathlib
from android.storage import app_storage_path

ANDROID_PATH = pathlib.Path(app_storage_path())
