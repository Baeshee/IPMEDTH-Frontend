from PyQt6.QtWidgets import QPushButton, QWidget, QHBoxLayout
from PyQt6 import uic

from components.menu import Menu
from components.mainHome import Main

class HomePage(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.menu = Menu()
        self.main = Main()
        
        wList = [self.menu, self.main]
        
        for w in wList:
            layout.addWidget(w)
            
        self.setLayout(layout)