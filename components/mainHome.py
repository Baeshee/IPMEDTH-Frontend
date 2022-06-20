from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
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
        self.toast.setHidden(True)
        
        
    def connectClickEvent(self):
        components = [
            self.metingBtnBig,
            self.resultBtnBig
        ]
        
        for comp in components:
            comp.mousePressEvent = partial(self.handleClickEvent, comp.objectName())


    def handleClickEvent(self, event, object):
        if event == 'metingBtnBig':
            self.app.meting.select.getPatients()
            self.app.stackedWidget.setCurrentIndex(2)
            self.app.meting.menu.metingBtn.setStyleSheet('background-color: #00aaa6;')
        if event == 'resultBtnBig':
            self.app.resultaten.main.loadData()
            self.app.stackedWidget.setCurrentIndex(3)
            self.app.resultaten.menu.resultatenBtn.setStyleSheet('background-color: #00aaa6;')
            
    def timer(self, text):
        if "created" in text:
            self.toast.setStyleSheet("background-color: #2abd13;")   
        else:
            self.toast.setStyleSheet("background-color: #bd1321;")
        
        self.toast.setText(text)
        self.toast.setHidden(False)
        
        timer = QTimer(self)
        timer.timeout.connect(self.setToHidden)
        timer.start(5000)
        
    def setToHidden(self):
        self.toast.setHidden(True)