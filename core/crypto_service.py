import os
import json
import base64

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from core.config import (
    PBKDF2_ITERATIONS,
    AES_KEY_LENGTH,
    SALT_LENGTH,
    NONCE_LENGTH
)


class CryptoService:
    @staticmethod
    def derive_key(master_password: str, salt: bytes) -> bytes:
        """
        Deriva una clave AES desde la contraseña maestra.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=AES_KEY_LENGTH,
            salt=salt,
            iterations=PBKDF2_ITERATIONS,
        )

        return kdf.derive(master_password.encode())

    @staticmethod
    def encrypt_data(data: dict, master_password: str) -> bytes:
        """
        Cifra un diccionario usando AES-GCM.
        """
        salt = os.urandom(SALT_LENGTH)
        nonce = os.urandom(NONCE_LENGTH)

        key = CryptoService.derive_key(master_password, salt)

        aesgcm = AESGCM(key)

        json_data = json.dumps(data).encode()

        encrypted = aesgcm.encrypt(nonce, json_data, None)

        payload = {
            "salt": base64.b64encode(salt).decode(),
            "nonce": base64.b64encode(nonce).decode(),
            "ciphertext": base64.b64encode(encrypted).decode()
        }

        return json.dumps(payload).encode()

    @staticmethod
    def decrypt_data(encrypted_data: bytes, master_password: str) -> dict:
        """
        Descifra datos AES-GCM.
        """
        payload = json.loads(encrypted_data.decode())

        salt = base64.b64decode(payload["salt"])
        nonce = base64.b64decode(payload["nonce"])
        ciphertext = base64.b64decode(payload["ciphertext"])

        key = CryptoService.derive_key(master_password, salt)

        aesgcm = AESGCM(key)

        decrypted = aesgcm.decrypt(nonce, ciphertext, None)

        return json.loads(decrypted.decode())