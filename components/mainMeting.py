from PyQt6.QtWidgets import QPushButton, QWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QPixmap, QColor, QImage
from PyQt6 import uic

import sys
import cv2 as cv
import numpy as np
import os

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    
    def run(self):
        self.cap = cv.VideoCapture(0)
        while True:
            ret, img = self.cap.read()
            # global cv_img
            # cv_img = img
            if ret:
                self.change_pixmap_signal.emit(img)
            
            if cv.waitKey(1) & 0xFF == ord('q'):
                self.stop()
                
    def stop(self):
        self.cap.release()
                
class Main(QWidget):
    def __init__(self, app):
        super(Main, self).__init__()
        uic.loadUi('layout/metingComponent.ui', self)
        self.app = app
        self.stream_label = self.videoLabel
        
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_stream)
        self.thread.start()
        
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