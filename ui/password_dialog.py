from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QTextEdit,
    QPushButton
)


class PasswordDialog(QDialog):
    def __init__(self, entry=None):
        super().__init__()

        self.entry = entry

        self.setWindowTitle("Contraseña")
        self.setFixedSize(420, 360)

        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: white;
            }

            QLineEdit, QTextEdit {
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

        self.site_input = QLineEdit()
        self.site_input.setPlaceholderText("Sitio / App")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario / Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Notas")

        if entry:
            self.site_input.setText(entry.site)
            self.username_input.setText(entry.username)
            self.password_input.setText(entry.password)
            self.notes_input.setText(entry.notes)

        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.accept)

        layout.addWidget(self.site_input)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.notes_input)
        layout.addWidget(save_btn)

        self.setLayout(layout)