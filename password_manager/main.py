# password_manager/main.py

import os
from .storage import StorageManager
from .auth import UserManager
import tkinter as tk
from .gui import LoginApp

KEY_FILE = "password_manager/data/clave.key"

# 👇 esta es la función que estaba faltando
def get_or_create_key():
    if not os.path.exists(KEY_FILE):
        key = StorageManager.generate_key()
        StorageManager.save_key(KEY_FILE, key)
        print("🔑 Clave generada.")
    else:
        print("🔑 Clave cargada.")
    return StorageManager.load_key(KEY_FILE)

# 👇 función principal del programa
def main():
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

# 👇 ejecuta el programa si este archivo se ejecuta como principal
if __name__ == "__main__":
    main()
