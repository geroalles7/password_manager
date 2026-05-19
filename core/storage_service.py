import json
from pathlib import Path

from core.config import USERS_FILE, DATA_DIR
from core.models import User, PasswordEntry
from core.crypto_service import CryptoService


class StorageService:
    @staticmethod
    def load_users() -> list[User]:
        """
        Carga usuarios desde users.json
        """
        if not USERS_FILE.exists():
            return []

        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [User(**user_data) for user_data in data.get("users", [])]

    @staticmethod
    def save_users(users: list[User]):
        """
        Guarda usuarios en users.json
        """
        data = {
            "users": [user.to_dict() for user in users]
        }

        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def user_exists(username: str) -> bool:
        users = StorageService.load_users()
        return any(user.username == username for user in users)

    @staticmethod
    def get_user(username: str) -> User | None:
        users = StorageService.load_users()

        for user in users:
            if user.username == username:
                return user

        return None

    @staticmethod
    def get_vault_path(username: str) -> Path:
        return DATA_DIR / f"{username}.vault"

    @staticmethod
    def create_empty_vault(username: str, master_password: str):
        """
        Crea vault vacío cifrado
        """
        vault_data = {
            "passwords": []
        }

        encrypted = CryptoService.encrypt_data(vault_data, master_password)

        vault_path = StorageService.get_vault_path(username)

        with open(vault_path, "wb") as f:
            f.write(encrypted)

    @staticmethod
    def load_vault(username: str, master_password: str) -> list[PasswordEntry]:
        """
        Carga contraseñas del usuario
        """
        vault_path = StorageService.get_vault_path(username)

        if not vault_path.exists():
            raise FileNotFoundError("Vault no encontrado.")

        with open(vault_path, "rb") as f:
            encrypted_data = f.read()

        decrypted = CryptoService.decrypt_data(encrypted_data, master_password)

        return [
            PasswordEntry.from_dict(entry)
            for entry in decrypted.get("passwords", [])
        ]

    @staticmethod
    def save_vault(username: str, master_password: str, entries: list[PasswordEntry]):
        """
        Guarda vault cifrado
        """
        vault_data = {
            "passwords": [entry.to_dict() for entry in entries]
        }

        encrypted = CryptoService.encrypt_data(vault_data, master_password)

        vault_path = StorageService.get_vault_path(username)

        with open(vault_path, "wb") as f:
            f.write(encrypted)