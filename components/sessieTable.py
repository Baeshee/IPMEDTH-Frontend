from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class SessieTable(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("component_ui/sessieTable.ui", self)
