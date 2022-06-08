from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5 import uic

class Main(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('layout/mainHome.ui', self)