from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

from functools import partial

class Main(QWidget):
    def __init__(self, app):
        super().__init__()
        uic.loadUi('layout/mainHome.ui', self)
        self.app = app
        self.metingIcon.setPixmap(QPixmap('icons/ui/meting_big_white.png'))
        self.resultIcon.setPixmap(QPixmap('icons/ui/results_big_white.png'))
        self.connectClickEvent()
        
        
    def connectClickEvent(self):
        components = [
            self.metingBtnBig,
            self.resultBtnBig
        ]
        
        for comp in components:
            comp.mousePressEvent = partial(self.handleClickEvent, comp.objectName())


    def handleClickEvent(self, event, object):
        if event == 'metingBtnBig':
            
            self.app.stackedWidget.setCurrentIndex(2)
        if event == 'metingBtnBig':
            self.app.stackedWidget.setCurrentIndex(3)