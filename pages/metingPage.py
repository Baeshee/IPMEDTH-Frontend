from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6 import uic

from components.menu import Menu
from components.mainMeting import Main

class MetingPage(QWidget):
    def __init__(self, app):
        super(MetingPage, self).__init__()
        self.initPage(app)
    
        
    def initPage(self, app):
        self.app = app
        self.menu = Menu(self.app)
        self.main = Main(self.app)
        wList = [self.menu, self.main]
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        for w in wList:
            layout.addWidget(w)

        self.setLayout(layout)