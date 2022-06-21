from PyQt5.QtWidgets import QHBoxLayout, QWidget

from components.mainHome import Main
from components.menu import Menu


class HomePage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.initPage(app)

    def initPage(self, app):
        self.app = app
        self.menu = Menu(self.app)
        self.main = Main(self.app)
        wList = [self.menu, self.main]

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        for w in wList:
            layout.addWidget(w)

        self.setLayout(layout)
