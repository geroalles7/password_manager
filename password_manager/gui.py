import tkinter as tk
from tkinter import messagebox, simpledialog
import os
from .auth import UserManager
from .storage import StorageManager
from .password_manager import PasswordManager
import tkinter.ttk as ttk


KEY_FILE = "password_manager/data/clave.key"

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Contraseñas - Login")
        self.root.geometry("300x200")

        self.key = self.get_or_create_key()
        self.user_manager = UserManager(self.key)

        self.build_ui()

    def get_or_create_key(self):
        if not os.path.exists(KEY_FILE):
            key = StorageManager.generate_key()
            StorageManager.save_key(KEY_FILE, key)
        return StorageManager.load_key(KEY_FILE)

    def build_ui(self):
        tk.Label(self.root, text="Usuario:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Contraseña:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Iniciar sesión", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Registrarse", command=self.register).pack()

    def login(self):
        user = self.username_entry.get()
        pw = self.password_entry.get()

        if self.user_manager.authenticate_user(user, pw):
            messagebox.showinfo("Éxito", f"¡Bienvenido {user}!")
            self.root.destroy()  # Cerramos ventana login
            main_window = tk.Tk()
            PasswordManagerApp(main_window, self.key, user)
            main_window.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def register(self):
        user = self.username_entry.get()
        pw = self.password_entry.get()

        success, msg = self.user_manager.register_user(user, pw)
        if success:
            messagebox.showinfo("Registrado", msg)
        else:
            messagebox.showwarning("Error", msg)


class PasswordManagerApp:
    def __init__(self, root, key, username):
        self.root = root
        self.root.title(f"Contraseñas de {username}")
        self.root.geometry("600x400")

        self.key = key
        self.username = username
        self.pw_manager = PasswordManager(key, username)

        self.build_ui()
        self.load_passwords()

    def build_ui(self):
        # Agregamos la columna "Nombre" y definimos las tres columnas
        self.tree = ttk.Treeview(self.root, columns=("Nombre", "Usuario", "Contraseña"), show="headings")

        # Configuramos los encabezados de las columnas
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Contraseña", text="Contraseña")

        # Configuramos ancho de las columnas
        self.tree.column("Nombre", width=150)
        self.tree.column("Usuario", width=150)
        self.tree.column("Contraseña", width=150)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        tk.Button(frame, text="Agregar", command=self.add_password).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Editar", command=self.edit_password).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Eliminar", command=self.delete_password).pack(side=tk.LEFT, padx=5)

        tk.Button(self.root, text="Cerrar sesión", command=self.logout).pack(pady=10)

    def load_passwords(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for idx, item in enumerate(self.pw_manager.passwords["contraseñas"]):
            self.tree.insert("", "end", iid=idx, values=(item["nombre"], item["usuario"], item["contraseña"]))


    def add_password(self):
        nombre = simpledialog.askstring("Nombre", "Nombre del sitio/app:")
        if not nombre:
            return
        usuario = simpledialog.askstring("Usuario", "Nombre de usuario:")
        if not usuario:
            return
        contraseña = simpledialog.askstring("Contraseña", "Contraseña:")
        if not contraseña:
            return

        self.pw_manager.add_password(nombre, usuario, contraseña)
        self.load_passwords()

    def edit_password(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccioná una contraseña para editar.")
            return
        index = int(selected[0])
        item = self.pw_manager.passwords["contraseñas"][index]

        nombre = simpledialog.askstring("Nombre", "Nombre del sitio/app:", initialvalue=item["nombre"])
        if not nombre:
            return
        usuario = simpledialog.askstring("Usuario", "Nombre de usuario:", initialvalue=item["usuario"])
        if not usuario:
            return
        contraseña = simpledialog.askstring("Contraseña", "Contraseña:", initialvalue=item["contraseña"])
        if not contraseña:
            return

        self.pw_manager.edit_password(index, nombre, usuario, contraseña)
        self.load_passwords()

    def delete_password(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccioná una contraseña para eliminar.")
            return
        index = int(selected[0])

        confirm = messagebox.askyesno("Confirmar", "¿Querés eliminar esta contraseña?")
        if confirm:
            self.pw_manager.delete_password(index)
            self.load_passwords()

    def logout(self):
        self.root.destroy()  # Cerramos ventana principal

        # Abrimos ventana login otra vez
        root = tk.Tk()
        from .gui import LoginApp  # Import local para evitar problemas circulares
        app = LoginApp(root)
        root.mainloop()
