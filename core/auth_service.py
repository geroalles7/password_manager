from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from core.config import (
    DEFAULT_ADMIN_USERNAME,
    DEFAULT_ADMIN_PASSWORD
)
from core.models import User
from core.storage_service import StorageService
from core.crypto_service import CryptoService


class AuthService:
    def __init__(self):
        self.password_hasher = PasswordHasher()
        self.ensure_admin_exists()

    def ensure_admin_exists(self):
        """
        Crea admin por defecto si no existe
        """
        if StorageService.user_exists(DEFAULT_ADMIN_USERNAME):
            return

        password_hash = self.password_hasher.hash(DEFAULT_ADMIN_PASSWORD)

        admin = User(
            username=DEFAULT_ADMIN_USERNAME,
            password_hash=password_hash,
            role="admin"
        )

        users = StorageService.load_users()
        users.append(admin)

        StorageService.save_users(users)
        StorageService.create_empty_vault(
            DEFAULT_ADMIN_USERNAME,
            DEFAULT_ADMIN_PASSWORD
        )

    def register_user(self, username: str, master_password: str):
        """
        Registra un nuevo usuario
        """
        if StorageService.user_exists(username):
            raise ValueError("El usuario ya existe.")

        password_hash = self.password_hasher.hash(master_password)

        user = User(
            username=username,
            password_hash=password_hash,
            role="user"
        )

        users = StorageService.load_users()
        users.append(user)

        StorageService.save_users(users)
        StorageService.create_empty_vault(username, master_password)

    def login(self, username: str, master_password: str) -> User:
        """
        Login usuario
        """
        user = StorageService.get_user(username)

        if not user:
            raise ValueError("Usuario no encontrado.")

        try:
            self.password_hasher.verify(
                user.password_hash,
                master_password
            )
        except VerifyMismatchError:
            raise ValueError("Contraseña incorrecta.")

        # Validación extra:
        # verifica que pueda abrir el vault
        StorageService.load_vault(username, master_password)

        return user

    def change_master_password(
        self,
        username: str,
        current_password: str,
        new_password: str
    ):
        """
        Cambia contraseña maestra
        """
        user = StorageService.get_user(username)

        if not user:
            raise ValueError("Usuario no encontrado.")

        try:
            self.password_hasher.verify(
                user.password_hash,
                current_password
            )
        except VerifyMismatchError:
            raise ValueError("Contraseña actual incorrecta.")

        entries = StorageService.load_vault(
            username,
            current_password
        )

        new_hash = self.password_hasher.hash(new_password)

        users = StorageService.load_users()

        for existing_user in users:
            if existing_user.username == username:
                existing_user.password_hash = new_hash
                break

        StorageService.save_users(users)

        StorageService.save_vault(
            username,
            new_password,
            entries
        )