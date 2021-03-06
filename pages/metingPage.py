from PyQt5.QtWidgets import QHBoxLayout, QStackedWidget, QWidget

from components.mainMeting import Main
from components.menu import Menu
from components.newPatient import NewPatient
from components.patientSelect import PatientSelect


class MetingPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.initPage(app)

    def initPage(self, app):
        self.app = app
        self.patient_id = ""
        self.stackedWidget = QStackedWidget()

        self.menu = Menu(self.app)
        self.main = Main(self.app, self)
        self.select = PatientSelect(self.app, self, self.main)
        self.new = NewPatient(self.app, self, self.main)

        self.stackedWidget.addWidget(self.select)
        self.stackedWidget.addWidget(self.new)
        self.stackedWidget.addWidget(self.main)

        wList = [self.menu, self.stackedWidget]

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        for w in wList:
            layout.addWidget(w)

        self.setLayout(layout)
