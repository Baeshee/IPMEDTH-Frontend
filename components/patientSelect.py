from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from PyQt5.QtGui import QIcon

from functools import partial
import os
import shutil

from handlers.requestHandlers import getPatientRequest

class PatientSelect(QWidget):
    def __init__(self, app, page, main):
        super().__init__()
        uic.loadUi('layout/patientSelect.ui', self)
        self.app = app
        self.page = page
        self.main = main
        self.patient_ids = {}
        self.connectBtn()
        
        self.searchBtn.setIcon(QIcon('icons/ui/search.png'))

    def connectBtn(self):
        buttons = [
            self.continueBtn,
            self.switchBtn
        ]
        
        for btn in buttons:
            btn.clicked.connect(partial(self.handleBtn, btn.objectName()))
        
        
    def handleBtn(self, name):
        if name == 'continueBtn':
            if self.patientList.currentItem():
                self.page.patient_id = self.get_key_from_patient(self.patientList.currentItem().text())
                if self.page.patient_id:
                    self.main.patientName.setText(self.patientList.currentItem().text())
                    self.patientList.clear()
                    if os.path.isdir("temp"):
                        shutil.rmtree("temp")
                    os.mkdir("temp")
                    self.main.thread.start()
                    self.page.stackedWidget.setCurrentIndex(2)
            else:
                print("Geen patient geselecteerd!")

        if name == "switchBtn":
            self.page.stackedWidget.setCurrentIndex(1)
            self.patientNameField.setText('')
    
    
            
    def getPatients(self):
        status, res = getPatientRequest(self.app.token_type, self.app.token)
        if status == 'Ok':
            for patient in res:
                self.patientList.addItem(patient['name'])
                self.patient_ids[patient['id']] = patient['name']
        else: 
            print(res)
            
    def get_key_from_patient(self, value):
        for key, val in self.patient_ids.items():
            if val == value:
                return key
        return None