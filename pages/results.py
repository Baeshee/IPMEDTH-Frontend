"""Results page."""

from PyQt5.QtWidgets import QHBoxLayout, QStackedWidget, QWidget

from components.mainResultaten import Main
from components.menu import Menu


class ResultsPage(QWidget):
    """Results page QWidget class."""

    def __init__(self, app):
        super().__init__()
        self.init_page(app)

    def init_page(self, app):
        """Initialize the page."""
        self.app = app
        self.patient_id = ""
        self.stacked_widget = QStackedWidget()

        self.menu = Menu(self.app)
        self.main = Main(self.app)

        w_list = [self.menu, self.main]

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        for item in w_list:
            layout.addWidget(item)

        self.setLayout(layout)
