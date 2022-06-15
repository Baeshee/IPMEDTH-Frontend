from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5 import uic

from functools import partial
import asyncio

from handlers.requestHandlers import loginRequest


class Main(QWidget):
    def __init__(self, app):
        super(Main, self).__init__()
        uic.loadUi("layout/loginSection.ui", self)
        self.app = app
        self.showHide.setPixmap(QPixmap("icons/ui/show.svg"))

        self.connectBtn()
        self.connectClickEvent()
        self.toast.setHidden(True)

    def connectClickEvent(self):
        self.showHide.mousePressEvent = partial(
            self.handleClickEvent, self.showHide.objectName()
        )
        self.passwordField.returnPressed.connect(self.handleLogin)

    def handleClickEvent(self, event, object):
        if event == "showHide":
            if self.passwordField.echoMode() == QLineEdit.EchoMode.Password:
                self.passwordField.setEchoMode(QLineEdit.EchoMode.Normal)
                self.showHide.setPixmap(QPixmap("icons/ui/hide.svg"))
            else:
                self.passwordField.setEchoMode(QLineEdit.EchoMode.Password)
                self.showHide.setPixmap(QPixmap("icons/ui/show.svg"))

    def connectBtn(self):
        self.loginBtn.clicked.connect(self.handleLogin)

    def handleLogin(self):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        status, res = asyncio.run(loginRequest(self.emailField.text(), self.passwordField.text()))
        if status == 'Ok':
            self.app.token = res[0]
            self.app.token_type = res[1]
            self.app.user = res[2]

            self.app.stackedWidget.setCurrentIndex(1)
            self.emailField.setText(""),
            self.passwordField.setText("")
        else:
            self.toast.setText(res)
            self.toast.setStyleSheet("background-color: #bd1321;")
            self.toast.setHidden(False)
