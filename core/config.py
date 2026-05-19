import os
import sys
from pathlib import Path


def get_app_data_dir():
    if getattr(sys, "frozen", False):
        base_path = Path(os.getenv("APPDATA")) / "PasswordManager"
    else:
        base_path = Path(__file__).resolve().parent.parent / "data"

    base_path.mkdir(exist_ok=True)
    return base_path


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path

    return Path(relative_path)


DATA_DIR = get_app_data_dir()

USERS_FILE = DATA_DIR / "users.json"

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin_2025"

PBKDF2_ITERATIONS = 600000
AES_KEY_LENGTH = 32
SALT_LENGTH = 16
NONCE_LENGTH = 12


def ensure_directories():
    DATA_DIR.mkdir(exist_ok=True)