from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDate
from PyQt5 import uic

from functools import partial
import os
import shutil
import asyncio

from handlers.requestHandlers import makePatientRequest

class NewPatient(QWidget):
    def __init__(self, app, page, main):
        super().__init__()
        uic.loadUi('layout/newPatient.ui', self)
        self.app = app
        self.page = page
        self.main = main
        self.connectBtn()
        self.toast.setHidden(True)
        
        self.dateField.setDate(QDate.currentDate())
        
    def connectBtn(self):
        buttons = [
            self.continueBtn,
            self.switchBtn
        ]
        
        for btn in buttons:
            btn.clicked.connect(partial(self.handleBtn, btn.objectName()))
        
    def handleBtn(self, name):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        if name == 'continueBtn':
            if self.patientNameField.text() != '' and self.emailField.text() != '' and self.dateField.date().toPyDate() != '':
                status, res = asyncio.run(makePatientRequest(self.app.token_type, self.app.token, self.patientNameField.text(), self.emailField.text(), self.dateField.date().toPyDate()))
                if status == 'Ok':
                    self.page.patient_id = res['data']['id']
                    self.main.patientName.setText(self.patientNameField.text())
                    self.patientNameField.setText('')
                    self.main.thread.start()
                    if os.path.isdir("temp"):
                        shutil.rmtree("temp")
                    os.mkdir("temp")
                    self.page.stackedWidget.setCurrentIndex(2)
                    self.page.main.timer(res['message'])
                else: 
                    self.toast.setText(res)
                    self.toast.setHidden(False)
            else:
                self.toast.setText("Alle velden moeten ingevuld zijn!")
                self.toast.setStyleSheet("background-color: #bd1321;")
                self.toast.setHidden(False)
            
        if name == "switchBtn":
            self.patientNameField.setText('')
            self.emailField.setText('')
            self.dateField.setDate(QDate.currentDate())
            self.page.stackedWidget.setCurrentIndex(0)
            
            
            