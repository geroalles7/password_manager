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
            self.root.destroy() 

            if user == "admin" and pw == "admin_2025":
                main_window = tk.Tk()
                AdminPanel(main_window, self.key)
                main_window.mainloop()
            else:
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
        self.root.geometry("800x400")

        self.key = key
        self.username = username
        self.pw_manager = PasswordManager(key, username)

        self.build_ui()
        self.load_passwords()

    def build_ui(self):
       
        self.tree = ttk.Treeview(self.root, columns=("Nombre", "Usuario", "Contraseña", "Notas"), show="headings")

        
        self.tree.column("Nombre", width=150, anchor="center")
        self.tree.column("Usuario", width=150, anchor="center")
        self.tree.column("Notas", width=200, anchor="center")
        self.tree.column("Contraseña", width=150, anchor="center")

        self.tree.heading("Nombre", text="Nombre", anchor="center")
        self.tree.heading("Usuario", text="Usuario", anchor="center")
        self.tree.heading("Notas", text="Notas", anchor="center")
        self.tree.heading("Contraseña", text="Contraseña", anchor="center")


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
            self.tree.insert("", "end", iid=idx, values=(item["nombre"], item["usuario"], item["contraseña"], item.get("notas", "")))


    def add_password(self):
        nombre = simpledialog.askstring("Nombre", "Nombre del sitio/app:", parent=self.root)
        if not nombre:
            return
        usuario = simpledialog.askstring("Usuario", "Nombre de usuario:", parent=self.root)
        if not usuario:
            return
        contraseña = simpledialog.askstring("Contraseña", "Contraseña:", parent=self.root)
        if not contraseña:
            return
        notas = simpledialog.askstring("Notas", "Notas u observaciones:", parent=self.root) or ""

        self.pw_manager.add_password(nombre, usuario, contraseña, notas)
        self.load_passwords()

    def edit_password(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccioná una contraseña para editar.", parent=self.root)
            return
        index = int(selected[0])
        item = self.pw_manager.passwords["contraseñas"][index]

        nombre = simpledialog.askstring("Nombre", "Nombre del sitio/app:", initialvalue=item["nombre"], parent=self.root)
        if not nombre:
            return
        usuario = simpledialog.askstring("Usuario", "Nombre de usuario:", initialvalue=item["usuario"], parent=self.root)
        if not usuario:
            return
        contraseña = simpledialog.askstring("Contraseña", "Contraseña:", initialvalue=item["contraseña"], parent=self.root)
        if not contraseña:
            return
        notas = simpledialog.askstring("Notas", "Notas u observaciones:", initialvalue=item.get("notas", ""), parent=self.root) or ""

        self.pw_manager.edit_password(index, nombre, usuario, contraseña, notas)
        self.load_passwords()

    def delete_password(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccioná una contraseña para eliminar.", parent=self.root)
            return
        index = int(selected[0])

        confirm = messagebox.askyesno("Confirmar", "¿Querés eliminar esta contraseña?", parent=self.root)
        if confirm:
            self.pw_manager.delete_password(index)
            self.load_passwords()

    def logout(self):
        self.root.destroy()  

        
        root = tk.Tk()
        from .gui import LoginApp
        app = LoginApp(root)
        root.mainloop()


class AdminPanel:
    def __init__(self, root, key):
        self.root = root
        self.root.title("Panel de Administrador")
        self.root.geometry("400x400")

        self.key = key
        self.user_manager = UserManager(key)

        self.build_ui()
        self.load_users()

    def build_ui(self):
        self.tree = ttk.Treeview(self.root, columns=("Usuario", "Contraseña"), show="headings")

        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Contraseña", text="Contraseña")

        self.tree.column("Usuario", width=150)
        self.tree.column("Contraseña", width=200)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        tk.Button(frame, text="Cambiar contraseña", command=self.change_password).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Cerrar sesión", command=self.logout).pack(side=tk.LEFT, padx=5)


    def load_users(self):
        self.user_manager.users = self.user_manager.load_users()

        self.tree.delete(*self.tree.get_children())

        for idx, (usuario, contraseña) in enumerate(self.user_manager.users.items()):
            if usuario != "admin" and usuario.strip() != "":
                iid = f"user_{idx}"
                self.tree.insert("", "end", iid=iid, values=(usuario, contraseña))






    def change_password(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccioná un usuario.")
            return

        usuario = self.tree.item(selected[0])['values'][0]
        nueva = simpledialog.askstring("Nueva contraseña", f"Nueva contraseña para {usuario}:")
        if not nueva:
            return

        self.user_manager.users = self.user_manager.load_users()
        self.user_manager.users[usuario] = nueva
        self.user_manager.save_users()
        self.load_users()
        messagebox.showinfo("Listo", f"Contraseña cambiada para {usuario}.")


    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        LoginApp(root)
        root.mainloop()
