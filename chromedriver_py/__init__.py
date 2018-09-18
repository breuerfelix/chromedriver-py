import os
import platform

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _get_filename():
    path = os.path.join(_BASE_DIR, "chromedriver")

    sys = platform.system()
    if sys == "Windows":
        path += ".exe"
    elif sys == "Darwin":
        path += "_mac"
    elif sys == "Linux":
        path += "_linux"

    return path

binary_path = _get_filename()
