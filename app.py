"""Main start application file."""

import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget

from pages.home import HomePage
from pages.login import LoginPage
from pages.measurement import MeasurementPage
from pages.results import ResultsPage


class App(QMainWindow):
    """The main app Qt class."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Handmetingen Tool")
        self.setWindowIcon(QtGui.QIcon("icons/app_icon.png"))
        self.setMinimumSize(1600, 900)
        QtGui.QFontDatabase.addApplicationFont("styles/fonts/Humanist521LightBT.ttf")
        self.init_ui()

        # Parameter storage
        self.token = ""
        self.token_type = ""
        self.user = ""

    def init_ui(self):
        """Initialize the UI."""
        self.stacked_widget = QStackedWidget()

        # Init widget
        self.login = LoginPage(self)
        self.home = HomePage(self)
        self.measurement = MeasurementPage(self)
        self.results = ResultsPage(self)

        # Add to stack
        self.stacked_widget.addWidget(self.login)
        self.stacked_widget.addWidget(self.home)
        self.stacked_widget.addWidget(self.measurement)
        self.stacked_widget.addWidget(self.results)

        # Set all widgets
        self.setCentralWidget(self.stacked_widget)
        with open("styles/index.css", encoding="utf-8") as stylesheet:
            self.setStyleSheet(stylesheet.read())


# Initialize the application
QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
app = QApplication(sys.argv)
AppWindow = App()
AppWindow.show()
app.exec()
