from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QMessageBox,
    QLabel
)

from core.storage_service import StorageService
from core.config import DATA_DIR


class AdminDialog(QDialog):
    def __init__(self, current_user):
        super().__init__()

        self.current_user = current_user

        self.setWindowTitle("Panel Administrador")
        self.resize(500, 500)

        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: white;
            }

            QLabel {
                font-size: 18px;
                font-weight: bold;
            }

            QListWidget {
                background-color: #2d2d2d;
                border: none;
                color: white;
                padding: 8px;
                border-radius: 8px;
            }

            QPushButton {
                background-color: #3a86ff;
                border: none;
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #2667cc;
            }
        """)

        layout = QVBoxLayout()

        title = QLabel("Usuarios registrados")

        self.user_list = QListWidget()

        delete_btn = QPushButton("🗑 Eliminar usuario")
        delete_btn.clicked.connect(self.delete_user)

        layout.addWidget(title)
        layout.addWidget(self.user_list)
        layout.addWidget(delete_btn)

        self.setLayout(layout)

        self.load_users()

    def load_users(self):
        self.user_list.clear()

        users = StorageService.load_users()

        for user in users:
            self.user_list.addItem(
                f"{user.username} ({user.role})"
            )

    def get_selected_username(self):
        item = self.user_list.currentItem()

        if not item:
            return None

        return item.text().split(" ")[0]

    def delete_user(self):
        username = self.get_selected_username()

        if not username:
            QMessageBox.warning(
                self,
                "Error",
                "Seleccione un usuario."
            )
            return

        if username == self.current_user.username:
            QMessageBox.warning(
                self,
                "Error",
                "No podés eliminarte a vos mismo."
            )
            return

        confirm = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Eliminar usuario '{username}'?"
        )

        if confirm != QMessageBox.Yes:
            return

        users = StorageService.load_users()
        users = [u for u in users if u.username != username]

        StorageService.save_users(users)

        vault_path = DATA_DIR / f"{username}.vault"

        if vault_path.exists():
            vault_path.unlink()

        QMessageBox.information(
            self,
            "OK",
            "Usuario eliminado correctamente."
        )

        self.load_users()