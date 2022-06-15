from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

from functools import partial

import time

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
            home_btn_time = time.time()
            if 'home_btn_time' in self.app.timestamps:
                self.app.timestamps['start_new_patient_time'] = (home_btn_time - self.app.start_time)
            self.app.timestamps['start_patient_select_time'] = (home_btn_time - self.app.start_time)
            
            self.app.meting.select.getPatients()
            self.app.stackedWidget.setCurrentIndex(2)
        if event == 'resultBtnBig':
            resultaten_btn = time.time()
            self.app.timestamps['resultaten_btn_time'] = (resultaten_btn - self.app.start_time)
            
            self.app.resultaten.main.loadData()
            self.app.stackedWidget.setCurrentIndex(3)
            
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