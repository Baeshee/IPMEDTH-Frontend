from PyQt5.QtWidgets import QWidget, QHBoxLayout, QStackedWidget
from PyQt5 import uic

from components.menu import Menu
from components.mainResultaten import Main


class ResultatenPage(QWidget):
    def __init__(self, app):
        super(ResultatenPage, self).__init__()
        self.initPage(app)

    def initPage(self, app):
        self.app = app
        self.patient_id = ""
        self.stackedWidget = QStackedWidget()

        self.menu = Menu(self.app)
        self.main = Main(self.app)

        wList = [self.menu, self.main]

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        for w in wList:
            layout.addWidget(w)

        self.setLayout(layout)
