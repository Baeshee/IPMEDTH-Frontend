"""Seccion table component."""

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class SessionTable(QWidget):
    """Session table Qwidget class."""

    def __init__(self):
        super().__init__()
        uic.loadUi("component_ui/sessieTable.ui", self)
