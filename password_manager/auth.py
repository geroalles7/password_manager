# password_manager/auth.py

import json
import os
from cryptography.fernet import Fernet
from .storage import StorageManager

USERS_FILE = "password_manager/data/usuarios.txt.enc"

class UserManager:
    def __init__(self, key: bytes):
        self.key = key
        self.cipher = Fernet(key)
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists(USERS_FILE):
            return {}

        data = StorageManager.load_encrypted_file(USERS_FILE, self.key)
        return json.loads(data) if data else {}

    def save_users(self):
        data = json.dumps(self.users)
        StorageManager.save_encrypted_file(USERS_FILE, data, self.key)

    def register_user(self, username, password):
        if username in self.users:
            return False, "El usuario ya existe."
        self.users[username] = password  # guardamos la contraseña simple por ahora
        self.save_users()
        return True, "Usuario registrado con éxito."

    def authenticate_user(self, username, password):
        # Acceso especial para el usuario admin
        if username == "admin" and password == "admin_2025":
            return True
        return self.users.get(username) == password

