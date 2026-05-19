from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QLineEdit,
    QHeaderView,
    QAbstractItemView,
    QApplication
)
from ui.admin_dialog import AdminDialog
from PySide6.QtCore import Qt

from core.storage_service import StorageService
from core.models import PasswordEntry

from ui.password_dialog import PasswordDialog
from ui.change_password_dialog import ChangePasswordDialog


class Dashboard(QWidget):
    def __init__(self, user, master_password):
        super().__init__()

        self.user = user
        self.master_password = master_password
        self.entries = []
        self.password_visible = False

        self.setWindowTitle("Password Manager")
        self.resize(1200, 700)

        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
                font-family: Segoe UI;
                font-size: 14px;
            }

            QPushButton {
                background-color: #2d2d2d;
                border: none;
                border-radius: 8px;
                padding: 12px;
                color: white;
                font-weight: bold;
                text-align: left;
            }

            QPushButton:hover {
                background-color: #3a86ff;
            }

            QTableWidget {
                background-color: #1e1e1e;
                border: none;
                gridline-color: #333;
            }

            QHeaderView::section {
                background-color: #2d2d2d;
                color: white;
                padding: 10px;
                border: none;
            }

            QLineEdit {
                background-color: #1e1e1e;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 10px;
                color: white;
            }
        """)

        main_layout = QHBoxLayout()

        # SIDEBAR
        sidebar = QVBoxLayout()

        title = QLabel("🔐 Password Manager")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        vault_btn = QPushButton("🔑 Contraseñas")
        vault_btn.clicked.connect(self.load_entries)

        account_btn = QPushButton("👤 Mi cuenta")
        account_btn.clicked.connect(self.change_master_password)

        admin_btn = None

        if self.user.role == "admin":
            admin_btn = QPushButton("⚙ Panel admin")
            admin_btn.clicked.connect(self.open_admin_panel)

        logout_btn = QPushButton("🚪 Logout")
        logout_btn.clicked.connect(self.logout)

        sidebar.addWidget(title)
        sidebar.addSpacing(30)
        sidebar.addWidget(vault_btn)
        sidebar.addWidget(account_btn)

        if admin_btn:
            sidebar.addWidget(admin_btn)
        sidebar.addStretch()
        sidebar.addWidget(logout_btn)

        # MAIN CONTENT
        content = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar sitio o usuario...")
        self.search_input.textChanged.connect(self.filter_entries)

        actions = QHBoxLayout()

        add_btn = QPushButton("➕ Nueva")
        add_btn.clicked.connect(self.add_password)

        edit_btn = QPushButton("✏ Editar")
        edit_btn.clicked.connect(self.edit_password)

        delete_btn = QPushButton("🗑 Eliminar")
        delete_btn.clicked.connect(self.delete_password)

        show_btn = QPushButton("👁 Mostrar")
        show_btn.clicked.connect(self.toggle_passwords)

        copy_pass_btn = QPushButton("📋 Copiar clave")
        copy_pass_btn.clicked.connect(self.copy_password)

        copy_user_btn = QPushButton("📋 Copiar usuario")
        copy_user_btn.clicked.connect(self.copy_username)

        actions.addWidget(add_btn)
        actions.addWidget(edit_btn)
        actions.addWidget(delete_btn)
        actions.addWidget(show_btn)
        actions.addWidget(copy_pass_btn)
        actions.addWidget(copy_user_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Sitio / App",
            "Usuario",
            "Contraseña",
            "Notas"
        ])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_password)

        content.addWidget(self.search_input)
        content.addLayout(actions)
        content.addWidget(self.table)

        main_layout.addLayout(sidebar, 1)
        main_layout.addLayout(content, 4)

        self.setLayout(main_layout)

        self.load_entries()

    def load_entries(self):
        try:
            self.entries = StorageService.load_vault(
                self.user.username,
                self.master_password
            )

            self.populate_table(self.entries)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def populate_table(self, entries):
        self.table.setRowCount(len(entries))

        for row, entry in enumerate(entries):
            password_text = entry.password if self.password_visible else "********"

            self.table.setItem(row, 0, QTableWidgetItem(entry.site))
            self.table.setItem(row, 1, QTableWidgetItem(entry.username))
            self.table.setItem(row, 2, QTableWidgetItem(password_text))
            self.table.setItem(row, 3, QTableWidgetItem(entry.notes))

    def filter_entries(self):
        query = self.search_input.text().lower()

        filtered = [
            entry for entry in self.entries
            if query in entry.site.lower()
            or query in entry.username.lower()
        ]

        self.populate_table(filtered)

    def add_password(self):
        dialog = PasswordDialog()

        if dialog.exec():
            new_entry = PasswordEntry(
                site=dialog.site_input.text(),
                username=dialog.username_input.text(),
                password=dialog.password_input.text(),
                notes=dialog.notes_input.toPlainText()
            )

            self.entries.append(new_entry)

            StorageService.save_vault(
                self.user.username,
                self.master_password,
                self.entries
            )

            self.load_entries()

    def edit_password(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Error", "Seleccione una contraseña.")
            return

        entry = self.entries[row]

        dialog = PasswordDialog(entry)

        if dialog.exec():
            entry.site = dialog.site_input.text()
            entry.username = dialog.username_input.text()
            entry.password = dialog.password_input.text()
            entry.notes = dialog.notes_input.toPlainText()

            StorageService.save_vault(
                self.user.username,
                self.master_password,
                self.entries
            )

            self.load_entries()

    def delete_password(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Error", "Seleccione una contraseña.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirmar",
            "¿Eliminar esta contraseña?"
        )

        if confirm != QMessageBox.Yes:
            return

        del self.entries[row]

        StorageService.save_vault(
            self.user.username,
            self.master_password,
            self.entries
        )

        self.load_entries()

    def toggle_passwords(self):
        self.password_visible = not self.password_visible
        self.load_entries()

    def copy_password(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Error",
                "Seleccione una contraseña."
            )
            return

        QApplication.clipboard().setText(
            self.entries[row].password
        )

        QMessageBox.information(
            self,
            "Copiado",
            "Contraseña copiada al portapapeles."
        )

    def copy_username(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Error",
                "Seleccione una contraseña."
            )
            return

        QApplication.clipboard().setText(
            self.entries[row].username
        )

        QMessageBox.information(
            self,
            "Copiado",
            "Usuario copiado al portapapeles."
        )

    def change_master_password(self):
        dialog = ChangePasswordDialog(self.user.username)

        if dialog.exec():
            QMessageBox.information(
                self,
                "Importante",
                "Volvé a iniciar sesión con tu nueva contraseña."
            )
            self.logout()

    def logout(self):
        from ui.login_window import LoginWindow

        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def open_admin_panel(self):
        dialog = AdminDialog(self.user)
        dialog.exec()