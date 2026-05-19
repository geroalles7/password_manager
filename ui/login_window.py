from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from core.auth_service import AuthService
from core.config import resource_path
from ui.register_dialog import RegisterDialog
from ui.dashboard import Dashboard


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.auth = AuthService()
        self.dashboard = None

        self.setWindowTitle("Password Manager")
        self.setFixedSize(450, 520)

        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
                font-family: Segoe UI;
            }

            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                padding-bottom: 20px;
            }

            QLineEdit {
                background-color: #1e1e1e;
                border: 1px solid #333;
                border-radius: 10px;
                padding: 12px;
                color: white;
                font-size: 14px;
            }

            QPushButton {
                background-color: #3a86ff;
                border: none;
                border-radius: 10px;
                padding: 12px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #2667cc;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)

        logo = QLabel()

        pixmap = QPixmap(str(resource_path("assets/icon.png")))
        pixmap = pixmap.scaled(
            100,
            100,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)

        title = QLabel("Password Manager")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña maestra")
        self.password_input.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Iniciar sesión")
        login_btn.clicked.connect(self.login)

        register_btn = QPushButton("Registrarse")
        register_btn.clicked.connect(self.open_register)

        copyright_label = QLabel(
            "© 2026 Alles Geronimo - Todos los derechos reservados"
        )
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("""
            color: #666;
            font-size: 11px;
        """)

        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_btn)
        layout.addWidget(register_btn)
        layout.addWidget(copyright_label)

        self.setLayout(layout)

    def open_register(self):
        dialog = RegisterDialog()

        if dialog.exec():
            QMessageBox.information(
                self,
                "Registro",
                "Ahora podés iniciar sesión."
            )

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(
                self,
                "Error",
                "Complete usuario y contraseña."
            )
            return

        try:
            user = self.auth.login(username, password)

            self.dashboard = Dashboard(user, password)
            self.dashboard.show()

            self.close()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )