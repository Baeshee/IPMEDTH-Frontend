"""Main login component."""

import asyncio
from functools import partial

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLineEdit, QWidget

from handlers.request_handlers import login_request


class Main(QWidget):
    """Main QWidget class."""

    def __init__(self, app):
        super().__init__()
        uic.loadUi("layout/loginSection.ui", self)
        self.app = app
        self.showHide.setPixmap(QPixmap("icons/ui/show.svg"))

        self.connect_btn()
        self.connect_click_event()
        self.toast.setHidden(True)

    def connect_click_event(self):
        """Connect the click event to the correct function."""
        self.showHide.mousePressEvent = partial(
            self.handle_click_event, self.showHide.objectName()
        )
        self.passwordField.returnPressed.connect(self.handle_login)

    def handle_click_event(self, event, click_object):
        """Handle the click event."""
        if event == "showHide":
            if self.passwordField.echoMode() == QLineEdit.EchoMode.Password:
                self.passwordField.setEchoMode(QLineEdit.EchoMode.Normal)
                self.showHide.setPixmap(QPixmap("icons/ui/hide.svg"))
            else:
                self.passwordField.setEchoMode(QLineEdit.EchoMode.Password)
                self.showHide.setPixmap(QPixmap("icons/ui/show.svg"))

    def connect_btn(self):
        """Connect the btn event to the correct function."""
        self.loginBtn.clicked.connect(self.handle_login)

    def handle_login(self):
        """Handle the login event."""
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        status, res = asyncio.run(
            login_request(self.emailField.text(), self.passwordField.text())
        )
        if status == "Ok":
            self.app.token = res[0]
            self.app.token_type = res[1]
            self.app.user = res[2]

            self.app.stacked_widget.setCurrentIndex(1)
            self.emailField.setText("")
            self.passwordField.setText("")
        else:
            self.toast.setText(res)
            self.toast.setStyleSheet("background-color: #bd1321;")
            self.toast.setHidden(False)
