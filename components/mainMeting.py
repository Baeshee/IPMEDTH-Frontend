from PyQt6.QtWidgets import QPushButton, QWidget
from PyQt6 import uic

class Main(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('layout/mainMeting.ui', self)