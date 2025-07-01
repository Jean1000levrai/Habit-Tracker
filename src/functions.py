import os
import sys



def resource_path(relative_path):
    try:
        # running from a app like pyinstaller
        base_path = sys._MEIPASS
    except AttributeError:
        # running from source
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

def resource_path2(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller uses this
    except AttributeError:
        base_path = os.path.abspath(".")  # fallback for dev mode
    return os.path.join(base_path, relative_path)


