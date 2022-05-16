from PyQt6.QtWidgets import QPushButton, QWidget, QHBoxLayout
from PyQt6 import uic

from components.menu import Menu
from components.mainMeting import Main

class MetingPage(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.menu = Menu()
        self.main = Main()
        
        wList = [self.menu, self.main]
        
        for w in wList:
            layout.addWidget(w)

        self.setLayout(layout)