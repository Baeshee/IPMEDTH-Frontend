from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

from functools import partial

from handlers.requestHandlers import logoutRequest

class Menu(QWidget):
    def __init__(self, app):
        super(Menu, self).__init__()
        uic.loadUi('layout/menu.ui', self)
        self.app = app
        self.connectBtn()
    
    
    def connectBtn(self):    
        buttons = [
            # Home
            self.homeBtn,
            self.metingBtn,
            self.resultatenBtn,
            self.logoutBtn,
        ]
    
        for btn in buttons:
            btn.clicked.connect(partial(self.handleBtn, btn.objectName()))
    
        
    def handleBtn(self, name):
        # Menu navigation
        if name == 'homeBtn':
            self.app.stackedWidget.setCurrentIndex(1)
            self.clear()
        elif name == 'metingBtn':
            self.app.meting.select.getPatients()
            self.app.meting.stackedWidget.setCurrentIndex(0)
            self.app.stackedWidget.setCurrentIndex(2)
        elif name == 'resultatenBtn':
            self.clear()
            self.app.stackedWidget.setCurrentIndex(3)
        
        # Logout request
        elif name == 'logoutBtn':
            status, res = logoutRequest(self.app.token_type, self.app.token)
            
            if status == 'Ok':
                self.app.stackedWidget.setCurrentIndex(0)
                
    def clear(self):
        self.app.meting.select.patientList.clear()
        self.app.meting.stackedWidget.setCurrentIndex(0)