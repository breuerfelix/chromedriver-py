import os
import platform

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))



def _get_filename():
    path = os.path.join(_BASE_DIR, "chromedriver_")

    machine = platform.machine().lower()
    sys = platform.system().lower()

    # windows
    if sys == "windows":
        if machine.endswith("64"):
            path += "win64.exe"
        else:
            path += "win32.exe"

    # mac
    elif sys == "darwin":
        path += "mac"
        if "arm" in machine:
            path += "-arm64"
        else:
            path += "-x64"

    # linux
    elif sys == "linux":
        if "arm" in machine:
            raise Exception("Google doesn't compile chromedriver versions for Linux ARM. Sorry!")
        if machine.endswith("32"):
            raise Exception("Google doesn't compile 32bit chromedriver versions for Linux. Sorry!")
        path += "linux64"

    # undefined
    else:
        raise Exception("Could not identify your system: " + sys)

    if not path or not os.path.isfile(path):
        msg = "Couldn't find a binary for your system: " + sys + " / " + machine + ". "
        msg += "Please create an Issue on github.com/breuerfelix/chromedriver-py and include this Message."
        raise Exception(msg)

    return path


binary_path = _get_filename()
