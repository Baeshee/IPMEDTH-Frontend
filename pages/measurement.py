"""Measurement page."""

from PyQt5.QtWidgets import QHBoxLayout, QStackedWidget, QWidget

from components.main_measurement import Main
from components.menu import Menu
from components.new_patient import NewPatient
from components.select_patient import PatientSelect


class MeasurementPage(QWidget):
    """Measurement page QWidget class."""

    def __init__(self, app):
        super().__init__()
        self.init_page(app)

    def init_page(self, app):
        """Initialize the page."""
        self.app = app
        self.patient_id = ""
        self.stacked_widget = QStackedWidget()

        self.menu = Menu(self.app)
        self.main = Main(self.app, self)
        self.select = PatientSelect(self.app, self, self.main)
        self.new = NewPatient(self.app, self, self.main)

        self.stacked_widget.addWidget(self.select)
        self.stacked_widget.addWidget(self.new)
        self.stacked_widget.addWidget(self.main)

        w_list = [self.menu, self.stacked_widget]

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        for item in w_list:
            layout.addWidget(item)

        self.setLayout(layout)
