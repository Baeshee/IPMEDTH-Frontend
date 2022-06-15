"""Menu component."""

import asyncio
from functools import partial

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget

from const import BASE_URL
from handlers.request_handlers import logout_request
from handlers.utils import open_url


class Menu(QWidget):
    """Menu QWidget class."""

    def __init__(self, app):
        super().__init__()
        uic.loadUi("layout/menu.ui", self)
        self.app = app
        self.connect_click_event()

        self.homeIcon.setPixmap(QPixmap("icons/ui/home_white.png"))
        self.metingIcon.setPixmap(QPixmap("icons/ui/meting_white.png"))
        self.resultatenIcon.setPixmap(QPixmap("icons/ui/results_white.png"))
        self.logoutIcon.setPixmap(QPixmap("icons/ui/logout_white.png"))
        self.profileIcon.setPixmap(QPixmap("icons/ui/account_circle_white.png"))

    def connect_click_event(self):
        """Connect the click event to the correct function."""
        buttons = [
            # Home
            self.homeBtn,
            self.metingBtn,
            self.resultatenBtn,
            self.logoutBtn,
            self.profileBtn,
        ]

        for btn in buttons:
            btn.mousePressEvent = partial(self.handle_click_event, btn.objectName())

    def handle_click_event(self, event, name):
        """Handle click event on buttons

        Args:
            event: id of the button
        """
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        # Menu navigation
        if event == "homeBtn":
            self.clear()
            self.app.stacked_widget.setCurrentIndex(1)
        elif event == "metingBtn":
            self.clear()
            self.app.measurement.select.get_patients()
            self.app.stacked_widget.setCurrentIndex(2)
        elif event == "resultatenBtn":
            self.clear()
            self.app.results.main.loadData()
            self.app.stacked_widget.setCurrentIndex(3)
        elif event == "profileBtn":
            self.clear()
            open_url(BASE_URL)

        # Logout request
        elif event == "logoutBtn":
            status, res = asyncio.run(
                logout_request(self.app.token_type, self.app.token)
            )

            if status == "Ok":
                self.app.stacked_widget.setCurrentIndex(0)

    def clear(self):
        """Clear the patientlist."""
        self.app.measurement.select.patientList.clear()
        self.app.measurement.main.closeMeting("menu")
