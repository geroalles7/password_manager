# password_manager/password_manager.py

import json
import os
from .storage import StorageManager

DATA_FOLDER = "password_manager/data"

class PasswordManager:
    def __init__(self, key: bytes, username: str):
        self.key = key
        self.username = username
        self.filepath = os.path.join(DATA_FOLDER, f"{username}_passwords.txt.enc")
        self.passwords = self.load_passwords()

    def load_passwords(self):
        if not os.path.exists(self.filepath):
            return {"contraseñas": []}

        data = StorageManager.load_encrypted_file(self.filepath, self.key)
        if data:
            return json.loads(data)
        else:
            return {"contraseñas": []}

    def save_passwords(self):
        data = json.dumps(self.passwords)
        StorageManager.save_encrypted_file(self.filepath, data, self.key)

    def add_password(self, nombre, usuario, contraseña):
        self.passwords["contraseñas"].append({
            "nombre": nombre,
            "usuario": usuario,
            "contraseña": contraseña
        })
        self.save_passwords()

    def edit_password(self, index, nombre, usuario, contraseña):
        if 0 <= index < len(self.passwords["contraseñas"]):
            self.passwords["contraseñas"][index] = {
                "nombre": nombre,
                "usuario": usuario,
                "contraseña": contraseña
            }
            self.save_passwords()

    def delete_password(self, index):
        if 0 <= index < len(self.passwords["contraseñas"]):
            self.passwords["contraseñas"].pop(index)
            self.save_passwords()
