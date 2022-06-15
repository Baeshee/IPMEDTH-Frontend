import asyncio
from functools import partial

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget

from const import BASE_URL
from handlers.requestHandlers import logoutRequest
from handlers.utils import open_url


class Menu(QWidget):
    def __init__(self, app):
        super(Menu, self).__init__()
        uic.loadUi("layout/menu.ui", self)
        self.app = app
        self.connectClickEvent()

        self.homeIcon.setPixmap(QPixmap("icons/ui/home_white.png"))
        self.metingIcon.setPixmap(QPixmap("icons/ui/meting_white.png"))
        self.resultatenIcon.setPixmap(QPixmap("icons/ui/results_white.png"))
        self.logoutIcon.setPixmap(QPixmap("icons/ui/logout_white.png"))
        self.profileIcon.setPixmap(QPixmap("icons/ui/account_circle_white.png"))

    def connectClickEvent(self):
        buttons = [
            # Home
            self.homeBtn,
            self.metingBtn,
            self.resultatenBtn,
            self.logoutBtn,
            self.profileBtn,
        ]

        for btn in buttons:
            btn.mousePressEvent = partial(self.handleClickEvent, btn.objectName())

    def handleClickEvent(self, event, name):
        """Handle click event on buttons

        Args:
            event: id of the button
        """
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        # Menu navigation
        if event == "homeBtn":
            self.clear()
            self.app.stackedWidget.setCurrentIndex(1)
        elif event == "metingBtn":
            self.clear()
            self.app.meting.select.getPatients()
            self.app.stackedWidget.setCurrentIndex(2)
        elif event == "resultatenBtn":
            self.clear()
            self.app.resultaten.main.loadData()
            self.app.stackedWidget.setCurrentIndex(3)
        elif event == "profileBtn":
            self.clear()
            open_url(BASE_URL)

        # Logout request
        elif event == "logoutBtn":
            status, res = asyncio.run(
                logoutRequest(self.app.token_type, self.app.token)
            )

            if status == "Ok":
                self.app.stackedWidget.setCurrentIndex(0)

    def clear(self):
        self.app.meting.select.patientList.clear()
        self.app.meting.main.closeMeting("menu")
