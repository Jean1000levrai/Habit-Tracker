import os
import sys
import shutil
from pathlib import Path



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
        base_path = sys._MEIPASS  # user install
    except AttributeError:
        base_path = os.path.abspath(".")  # dev mode in ide
    return os.path.join(base_path, relative_path)


def get_user_data_dir():
    """Returns platform-specific writable user data directory."""
    if sys.platform == 'win32':
        return os.getenv('APPDATA') or str(Path.home() / 'AppData' / 'Roaming')
    else:
        return str(Path.home() / '.habit_tracker')

def get_writable_db_path(db_filename):
    """Ensure a writable copy of a DB exists in user directory and return its path."""
    user_dir = Path(get_user_data_dir())
    user_dir.mkdir(parents=True, exist_ok=True)

    dest_db_path = user_dir / db_filename

    if not dest_db_path.exists():
        template_path = resource_path2(f"data/{db_filename}")
        shutil.copyfile(template_path, dest_db_path)

    return str(dest_db_path)


