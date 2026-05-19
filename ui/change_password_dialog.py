from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox
)

from core.auth_service import AuthService


class ChangePasswordDialog(QDialog):
    def __init__(self, username):
        super().__init__()

        self.username = username
        self.auth = AuthService()

        self.setWindowTitle("Cambiar contraseña maestra")
        self.setFixedSize(420, 280)

        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: white;
            }

            QLineEdit {
                background-color: #2d2d2d;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }

            QPushButton {
                background-color: #3a86ff;
                border: none;
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #2667cc;
            }
        """)

        layout = QVBoxLayout()

        self.current_password = QLineEdit()
        self.current_password.setPlaceholderText("Contraseña actual")
        self.current_password.setEchoMode(QLineEdit.Password)

        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Nueva contraseña")
        self.new_password.setEchoMode(QLineEdit.Password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirmar nueva contraseña")
        self.confirm_password.setEchoMode(QLineEdit.Password)

        save_btn = QPushButton("Cambiar contraseña")
        save_btn.clicked.connect(self.change_password)

        layout.addWidget(self.current_password)
        layout.addWidget(self.new_password)
        layout.addWidget(self.confirm_password)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def change_password(self):
        current = self.current_password.text()
        new = self.new_password.text()
        confirm = self.confirm_password.text()

        if not current or not new:
            QMessageBox.warning(
                self,
                "Error",
                "Complete todos los campos."
            )
            return

        if new != confirm:
            QMessageBox.warning(
                self,
                "Error",
                "Las contraseñas no coinciden."
            )
            return

        try:
            self.auth.change_master_password(
                self.username,
                current,
                new
            )

            QMessageBox.information(
                self,
                "OK",
                "Contraseña maestra actualizada."
            )

            self.accept()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )