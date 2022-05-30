from PyQt6.QtWidgets import QPushButton, QWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QPixmap, QColor, QImage
from PyQt6 import uic

import sys
import cv2 as cv
import numpy as np
import shutil
from functools import partial
from PIL import Image
import time

from handlers.requestHandlers import uploadRequest, sessionRequest
from handlers.hand_detect_module import handDetect

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    
    def __init__(self):
        super(VideoThread, self).__init__()
        self.detector = handDetect(detectCon=0.8, maxHands=2)
    
    def run(self):
        self.cap = cv.VideoCapture(0)
        while True:
            ret, img = self.cap.read()
            hands, img = self.detector.staticImage(img)
            global handData
            handData = hands
            
            global handImg
            handImg = img
            
            if ret:
                self.change_pixmap_signal.emit(img)
                
            
            if cv.waitKey(1) & 0xFF == ord('q'):
                self.stop()
                
    def stop(self):
        self.cap.release()
                
class Main(QWidget):
    def __init__(self, app, page):
        super(Main, self).__init__()
        uic.loadUi('layout/metingComponent.ui', self)
        self.app = app
        self.page = page
        self.connectBtn();
        self.stream_label = self.videoLabel
        
        self.resultaten = {}
        self.imageNames = {}
        
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_stream)
        
    def connectBtn(self):    
        buttons = [
            self.duimView,
            self.pinkView,
            self.vingerView,
            self.rugView,
        ]
    
        for btn in buttons:
            btn.clicked.connect(partial(self.handleBtn, btn.objectName()))
        
        # Isolated calls
        self.backBtn.clicked.connect(self.back)
        self.uploadBtn.clicked.connect(self.upload)

    
    def back(self):
        self.page.patient_id = ''
        self.app.meting.select.getPatients()
        self.thread.exit()
        self.page.stackedWidget.setCurrentIndex(0)
        
        
    def handleBtn(self, name):
        sender = self.sender()
        if len(handData) != 0:
            data = handData
            print('Meting geslaagd!')
        else:
            print('Meting mislukt!')
            return
        img = Image.fromarray(cv.cvtColor(handImg, cv.COLOR_BGR2RGB))
        
        if name == 'duimView':
            data["hand_view"] = "thumb_side"
            self.resultaten["thumbView"] = data
            path = "temp/thumb_view.png"
            
            img.save(path, format="PNG")
            self.imageNames["thumbView"] = path
        elif name == 'pinkView':
            data["hand_view"] = "pink_side"
            self.resultaten['pinkView'] = data
            path = "temp/pink_view.png"
            
            img.save(path, format="PNG")
            self.imageNames['pinkView'] = path    
        elif name == 'vingerView':
            data["hand_view"] = "finger_side"
            self.resultaten['fingerView'] = data
            path = "temp/finger_view.png"
            
            img.save(path, format="PNG")
            self.imageNames['fingerView'] = path
        elif name == 'rugView':
            data["hand_view"] = "back_side"
            self.resultaten['backView'] = data
            path = "temp/back_view.png"
            
            img.save(path, format="PNG")
            self.imageNames['backView'] = path
        
    def upload(self):
        status, s_id = sessionRequest(self.app.token_type, self.app.token, self.page.patient_id)
        if status == 'Ok':
            for key in self.resultaten.keys():
                status, res = uploadRequest(self.app.token_type, self.app.token, s_id, self.resultaten[key], self.imageNames[key])
                if status == 'Failed':
                    print(res)
                    break                    
            
            self.thread.exit()
            self.page.stackedWidget.setCurrentIndex(0)
            self.app.stackedWidget.setCurrentIndex(1)
            shutil.rmtree("temp") 
        else: 
            print(res)
        
    @pyqtSlot(np.ndarray)
    def update_stream(self, img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(img)
        self.stream_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        # p = convert_to_Qt_format.scaled(self.stream_label.geometry().width(), self.stream_label.geometry().height(), Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(convert_to_Qt_format)