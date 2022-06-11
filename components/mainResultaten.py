from PyQt5 import QtWidgets, Qt, QtCore
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QFont

from functools import partial
from handlers.requestHandlers import getPatientRequest
from components.sessieTable import SessieTable

class Main(QWidget):
    def __init__(self, app):
        super().__init__()
        uic.loadUi('layout/mainResultaten.ui', self)
        self.app = app
        self.sessieTable = SessieTable()
        self.patient_data = []
        self.sessiesTabLayout.setContentsMargins(0,0,0,0)
        
        self.placeholder = QLabel('Deze patient heeft nog geen sessies')
        self.placeholder.setAlignment(Qt.Qt.AlignCenter)
        self.placeholder.setFont(QFont('Calibri', 24))
        self.patientNameField.textChanged.connect(self.on_search)
        
    def loadData(self):
        status, res = getPatientRequest(self.app.token_type, self.app.token)
        if status == 'Ok':
            row = 0
            self.patientTable.setRowCount(len(res))
            for patient in res:
                self.patientTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(patient['id'])))
                self.patientTable.setItem(row, 1, QtWidgets.QTableWidgetItem(patient['name']))
                self.patientTable.setItem(row, 2, QtWidgets.QTableWidgetItem(patient['email']))
                self.patientTable.setItem(row, 3, QtWidgets.QTableWidgetItem(str(len(patient['sessions']))))
                self.patientTable.setItem(row, 4, QtWidgets.QTableWidgetItem(patient['date_of_birth']))
                row = row+1
                
                self.patient_data.append(patient)
                self.connectEvents() 
        else: 
            print(res)
            
    def connectEvents(self):
        self.patientTable.doubleClicked.connect(self.set_sessions)
            
    def set_sessions(self):
        if self.sessiesTabLayout.itemAt(0):
            for i in range(self.sessiesTabLayout.count()):
                self.sessiesTabLayout.itemAt(i).widget().setParent(None)
                
        if len(self.patient_data[self.patientTable.currentRow()]['sessions']) == 0:
            self.sessiesTabLayout.addWidget(self.placeholder)
        else:
            self.sessiesTabLayout.addWidget(self.sessieTable)
            row = 0
            self.sessieTable.table.setRowCount(len(self.patient_data[self.patientTable.currentRow()]['sessions']))
            for session in self.patient_data[self.patientTable.currentRow()]['sessions'] :
                self.sessieTable.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(session['id'])))
                self.sessieTable.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(len(session['measurements']))))
                self.sessieTable.table.setItem(row, 2, QtWidgets.QTableWidgetItem(session['date']))
                row = row+1
                
    @QtCore.pyqtSlot()
    def on_search(self):
        text = self.patientNameField.text()
        for row in range(self.patientTable.rowCount()):
            item = self.patientTable.item(row, 1)
            if text:
                self.patientTable.setRowHidden(row, not self.filter(text, item.text()))
            else:
                self.patientTable.setRowHidden(row, False)
    
    def filter(self, text, keywords):
        return text.lower() in keywords.lower()