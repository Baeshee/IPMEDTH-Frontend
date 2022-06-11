from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

class SessieTable(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('component_ui/sessieTable.ui', self)