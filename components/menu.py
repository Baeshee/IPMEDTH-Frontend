from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

from functools import partial

from handlers.requestHandlers import logoutRequest

class Menu(QWidget):
    def __init__(self, app):
        super(Menu, self).__init__()
        uic.loadUi('layout/menu.ui', self)
        self.app = app
        self.connectClickEvent()
        
        self.homeIcon.setPixmap(QPixmap('icons/ui/home_white.png'))
        self.metingIcon.setPixmap(QPixmap('icons/ui/meting_white.png'))
        self.resultatenIcon.setPixmap(QPixmap('icons/ui/results_white.png'))
        self.logoutIcon.setPixmap(QPixmap('icons/ui/logout_white.png'))
    
    
    def connectClickEvent(self):    
        buttons = [
            # Home
            self.homeBtn,
            self.metingBtn,
            self.resultatenBtn,
            self.logoutBtn,
        ]
    
        for btn in buttons:
            btn.mousePressEvent = partial(self.handleClickEvent, btn.objectName())
    
        
    def handleClickEvent(self, event, name):
        # Menu navigation
        if event == 'homeBtn':
            self.clear()
            self.app.stackedWidget.setCurrentIndex(1)
        elif event == 'metingBtn':
            self.clear()
            self.app.meting.select.getPatients()
            self.app.stackedWidget.setCurrentIndex(2)
        elif event == 'resultatenBtn':
            self.clear()
            self.app.resultaten.main.loadData()
            self.app.stackedWidget.setCurrentIndex(3)
        
        # Logout request
        elif event == 'logoutBtn':
            status, res = asyncio.run(logoutRequest(self.app.token_type, self.app.token))
            
            if status == 'Ok':
                self.app.stackedWidget.setCurrentIndex(0)
                
    def clear(self):
        self.app.meting.select.patientList.clear()
        self.app.meting.main.closeMeting('menu')