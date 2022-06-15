"""Main home component."""

from functools import partial

from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget


class Main(QWidget):
    """Main QWidget class."""

    def __init__(self, app):
        super().__init__()
        uic.loadUi("layout/mainHome.ui", self)
        self.app = app
        self.metingIcon.setPixmap(QPixmap("icons/ui/meting_big_white.png"))
        self.resultIcon.setPixmap(QPixmap("icons/ui/results_big_white.png"))
        self.connect_click_event()
        self.toast.setHidden(True)

    def connect_click_event(self):
        """Connect the click event to the correct function."""
        components = [self.metingBtnBig, self.resultBtnBig]

        for comp in components:
            comp.mousePressEvent = partial(self.handle_click_event, comp.objectName())

    def handle_click_event(self, event, click_object):
        """Handle the click event."""
        if event == "metingBtnBig":
            self.app.measurement.select.get_patients()
            self.app.stacked_widget.setCurrentIndex(2)
        if event == "resultBtnBig":
            self.app.results.main.loadData()
            self.app.stacked_widget.setCurrentIndex(3)

    def timer(self, text):
        """Set the toast and timer."""
        if "created" in text:
            self.toast.setStyleSheet("background-color: #2abd13;")
        else:
            self.toast.setStyleSheet("background-color: #bd1321;")

        self.toast.setText(text)
        self.toast.setHidden(False)

        timer = QTimer(self)
        timer.timeout.connect(self.set_to_hidden)
        timer.start(5000)

    def set_to_hidden(self):
        """Set the toast to hidden."""
        self.toast.setHidden(True)
