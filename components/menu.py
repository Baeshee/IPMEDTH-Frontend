from PyQt6.QtWidgets import QPushButton, QWidget
from PyQt6 import uic

class Menu(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('layout/menu.ui', self)