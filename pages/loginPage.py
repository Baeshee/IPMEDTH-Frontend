from PyQt5.QtWidgets import QHBoxLayout, QWidget

from components.mainLogin import Main


class LoginPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.initPage(app)

    def initPage(self, app):
        self.app = app
        self.login = Main(app)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.login)

        self.setLayout(layout)
