from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDate
from PyQt5 import uic

from functools import partial
import os
import shutil

from handlers.requestHandlers import makePatientRequest

class NewPatient(QWidget):
    def __init__(self, app, page, main):
        super().__init__()
        uic.loadUi('layout/newPatient.ui', self)
        self.app = app
        self.page = page
        self.main = main
        self.connectBtn()
        
        self.dateField.setDate(QDate.currentDate())
        
    def connectBtn(self):
        buttons = [
            self.continueBtn,
            self.switchBtn
        ]
        
        for btn in buttons:
            btn.clicked.connect(partial(self.handleBtn, btn.objectName()))
        
    def handleBtn(self, name):
        if name == 'continueBtn':
            status, res = makePatientRequest(self.app.token_type, self.app.token, self.patientNameField.text(), self.emailField.text(), self.dateField.date().toPyDate())
            if status == 'Ok':
                self.page.patient_id = res
                self.main.patientName.setText(self.patientNameField.text())
                self.patientNameField.setText('')
                self.main.thread.start()
                if os.path.isdir("temp"):
                    shutil.rmtree("temp")
                os.mkdir("temp")
                self.page.stackedWidget.setCurrentIndex(2)
            else: 
                print(res)
            
        if name == "switchBtn":
            self.patientNameField.setText('')
            self.emailField.setText('')
            self.dateField.setDate(QDate.currentDate())
            self.page.stackedWidget.setCurrentIndex(0)
            
            
            