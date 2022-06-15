"""Login page."""

from PyQt5.QtWidgets import QHBoxLayout, QWidget

from components.main_login import Main


class LoginPage(QWidget):
    """Login page QWidget class."""

    def __init__(self, app):
        super().__init__()
        self.init_page(app)

    def init_page(self, app):
        """Initialize the page."""
        self.app = app
        self.login = Main(app)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.login)

        self.setLayout(layout)
