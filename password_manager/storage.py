from cryptography.fernet import Fernet

class StorageManager:

    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    @staticmethod
    def save_key(path, key):
        with open(path, 'wb') as f:
            f.write(key)

    @staticmethod
    def load_key(path):
        with open(path, 'rb') as f:
            return f.read()

    @staticmethod
    def save_encrypted_file(path, data, key):
        cipher = Fernet(key)
        encrypted = cipher.encrypt(data.encode())
        with open(path, 'wb') as f:
            f.write(encrypted)

    @staticmethod
    def load_encrypted_file(path, key):
        try:
            with open(path, 'rb') as f:
                encrypted = f.read()
            cipher = Fernet(key)
            return cipher.decrypt(encrypted).decode()
        except Exception:
            return None
