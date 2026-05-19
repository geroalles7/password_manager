from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

from core.auth_service import AuthService


class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.auth = AuthService()

        self.setWindowTitle("Registro")
        self.setFixedSize(350, 250)

        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: white;
            }

            QLineEdit {
                background-color: #2d2d2d;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 8px;
                color: white;
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

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña maestra")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirmar contraseña")
        self.confirm_input.setEchoMode(QLineEdit.Password)

        register_btn = QPushButton("Registrarse")
        register_btn.clicked.connect(self.register_user)

        layout.addWidget(QLabel("Crear cuenta"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_input)
        layout.addWidget(register_btn)

        self.setLayout(layout)

    def register_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Complete todos los campos.")
            return

        if password != confirm:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden.")
            return

        try:
            self.auth.register_user(username, password)
            QMessageBox.information(self, "OK", "Usuario creado correctamente.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))