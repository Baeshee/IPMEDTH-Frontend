from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5 import uic

from functools import partial

from handlers.requestHandlers import loginRequest

class Main(QWidget):
    def __init__(self, app):
        super(Main, self).__init__()
        uic.loadUi('layout/loginSection.ui', self)
        self.app = app
        self.showHide.setPixmap(QPixmap('icons/show.png'))
        
        self.connectBtn()
        self.connectClickEvent()
        
        
    def connectClickEvent(self):
        self.showHide.mousePressEvent = partial(self.handleClickEvent, self.showHide.objectName())
        self.passwordField.returnPressed.connect(self.handleLogin)


    def handleClickEvent(self, event, object):
        if event == 'showHide':
            if self.passwordField.echoMode() == QLineEdit.EchoMode.Password:
                self.passwordField.setEchoMode(QLineEdit.EchoMode.Normal)
                self.showHide.setPixmap(QPixmap('icons/hide.png'))
            else: 
                self.passwordField.setEchoMode(QLineEdit.EchoMode.Password)
                self.showHide.setPixmap(QPixmap('icons/show.png'))
    
        
    def connectBtn(self):    
        self.loginBtn.clicked.connect(self.handleLogin)
    
        
    def handleLogin(self):
        # status, res = loginRequest(self.emailField.text(), self.passwordField.text())
        # if status == 'Ok':
        #     self.app.token = res[0]
        #     self.app.token_type = res[1]
        #     self.app.user = res[2]
            
            self.app.stackedWidget.setCurrentIndex(1)
        #     self.emailField.setText(''),
        #     self.passwordField.setText('') 
        # else: 
        #     print(res)