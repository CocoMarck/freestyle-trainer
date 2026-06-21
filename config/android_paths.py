# Android configs
import pathlib
from android.storage import app_storage_path
from jnius import autoclass

Environment = autoclass("android.os.Environment")

ANDROID_PRIVATE_PATH = pathlib.Path(app_storage_path())

music_dir_type = Environment.DIRECTORY_MUSIC
public_music_java_path = Environment.getExternalStoragePublicDirectory(music_dir_type).getAbsolutePath()

ANDROID_PUBLIC_MUSIC_PATH = pathlib.Path(public_music_java_path)

INTERNAL_STORAGE_ROOT = Environment.getExternalStorageDirectory().toString()

ANDROID_LEGACY_ROOT = Environment.getExternalStorageDirectory().getAbsolutePath()
