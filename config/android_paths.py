# Android configs
import pathlib
from android.storage import app_storage_path
from jnius import autoclass

Environment = autoclass("android.os.Environment")

ANDROID_PATH = pathlib.Path(app_storage_path())
EXTERNAL_DIR = Environment.getExternalStorageDirectory().getAbsolutePath()
