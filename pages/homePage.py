from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout
from PyQt5 import uic

from components.menu import Menu
from components.mainHome import Main

class HomePage(QWidget):
    def __init__(self, app):
        super(HomePage, self).__init__()
        self.initPage(app)
    
        
    def initPage(self, app):
        self.app = app
        self.menu = Menu(self.app)
        self.main = Main()
        wList = [self.menu, self.main]
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
                
        for w in wList:
            layout.addWidget(w)
            
        self.setLayout(layout)