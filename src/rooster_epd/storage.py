"""Shared paths and save-file helpers for Rooster-EPD."""

from json import dump, load
from os import environ
from pathlib import Path

# Where runtime data lives. The systemd services use /var/lib/rooster-epd;
# set ROOSTER_EPD_DATA to use another folder (handy during development).
DATA_DIR = Path(environ.get('ROOSTER_EPD_DATA', '/var/lib/rooster-epd'))

SAVE_PATH = DATA_DIR / 'save.json'
PASSWORD_PATH = DATA_DIR / 'password.pw'
STORAGE_SECRET_PATH = DATA_DIR / 'storage_secret.txt'

# Files that ship inside the package
FONT_PATH = Path(__file__).parent / 'assets' / 'om_thick_plain.ttf'


def new_save() -> dict:
    """Return an empty save file structure."""
    return {'templates': {},
            'starttime': 0,
            'endtime': 0,
            'token': '',
            'school': '',
            'notes': ['', '', '', '', '', '', ''],
            'appointments': []}


def write_save(save: dict) -> None:
    """Write the save file to disk."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(SAVE_PATH, 'w') as file:
        dump(save, file, indent=4)


def load_save() -> dict:
    """Load the save file, creating a new one if it doesn't exist yet."""
    if SAVE_PATH.is_file():
        print('Loading save file')
        with open(SAVE_PATH, 'r') as file:
            return load(file)

    print('Generating new save file')
    save = new_save()
    write_save(save)
    return save
