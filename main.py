import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from core.config import ensure_directories, resource_path
from core.auth_service import AuthService
from ui.login_window import LoginWindow


def main():
    ensure_directories()

    AuthService()

    app = QApplication(sys.argv)

    app.setWindowIcon(
        QIcon(str(resource_path("assets/icon.ico")))
    )

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()