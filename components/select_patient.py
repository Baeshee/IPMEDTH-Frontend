"""Select patient component."""

import asyncio
import os
import shutil
from functools import partial

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QWidget

from handlers.request_handlers import get_patient_request


class PatientSelect(QWidget):
    """Patient select QWidget class."""

    def __init__(self, app, page, main):
        super().__init__()
        uic.loadUi("layout/patientSelect.ui", self)
        self.app = app
        self.page = page
        self.main = main
        self.patient_ids = {}
        self.connect_btn()
        self.connect_click_event()
        self.toast.setHidden(True)

    def connect_click_event(self):
        """Connect the click event to the correct function."""
        self.patientNameField.textChanged.connect(self.on_search)

    def connect_btn(self):
        """Connect the buttons to the correct function."""
        buttons = [self.continueBtn, self.switchBtn]

        for btn in buttons:
            btn.clicked.connect(partial(self.handle_btn, btn.objectName()))

    def handle_btn(self, name):
        """Handle the button events."""
        if name == "continueBtn":
            if self.patientList.currentItem():
                self.page.patient_id = self.get_key_from_patient(
                    self.patientList.currentItem().text()
                )
                if self.page.patient_id:
                    self.main.patientName.setText(self.patientList.currentItem().text())
                    self.patientList.clear()
                    if os.path.isdir("temp"):
                        shutil.rmtree("temp")
                    os.mkdir("temp")
                    self.main.thread.start()
                    self.page.stacked_widget.setCurrentIndex(2)
            else:
                self.toast.setStyleSheet("background-color: #bd1321;")
                self.toast.setText("Geen patient geselecteerd!")
                self.toast.setHidden(False)

        if name == "switchBtn":
            self.page.stacked_widget.setCurrentIndex(1)
            self.patientNameField.setText("")

    def get_patients(self):
        """Get the patients from the API."""
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        status, res = asyncio.run(
            get_patient_request(self.app.token_type, self.app.token)
        )
        if status == "Ok":
            for patient in res:
                self.patientList.addItem(patient["name"])
                self.patient_ids[patient["id"]] = patient["name"]
        else:
            print(res)

    def get_key_from_patient(self, value):
        """Get the key from the patient."""
        for key, val in self.patient_ids.items():
            if val == value:
                return key
        return None

    @QtCore.pyqtSlot()
    def on_search(self):
        """Search for a patient in QtCore."""
        text = self.patientNameField.text()
        for row in range(self.patientList.count()):
            item = self.patientList.item(row)
            if text:
                item.setHidden(not self.filter(text, item.text()))
            else:
                item.setHidden(False)

    def filter(self, text, keywords):
        """Filter the patient list."""
        return text.lower() in keywords.lower()
