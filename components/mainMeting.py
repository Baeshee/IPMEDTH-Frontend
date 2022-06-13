from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5 import uic, Qt

import cv2 as cv
import numpy as np
import shutil
from functools import partial
from PIL import Image
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import pandas as pd

from handlers.requestHandlers import uploadRequest, sessionRequest
from handlers.hand_detect_module import handDetect
from handlers.modelHandler import PandasModel

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    def __init__(self):
        super(VideoThread, self).__init__()
        self.detector = handDetect(detectCon=0.8, maxHands=2)
        self.stop = False
        self.cap = None
    
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
                
            if self.stop == True:
                break
                
    def releaseCap(self):
        if self.cap is not None:
            self.stop = True
            self.cap.release()
            self.stop = False
        else:
            return  
class Main(QWidget):
    def __init__(self, app, page):
        super(Main, self).__init__()
        uic.loadUi('layout/metingComponent.ui', self)
        self.app = app
        self.page = page
        self.connectBtn();
        self.stream_label = self.videoLabel
        self.setHidden()
        
        self.resultaten = {}
        self.imageNames = {}
        
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_stream)
        
    def setHidden(self):
        self.toast.setHidden(True)
        self.tabWidget.setTabEnabled(1,False)
        for i in range(4):
            self.nestedTabWidget.setTabEnabled(i,False)
        
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
        self.closeMeting('back')
        
    def handleBtn(self, name):
        sender = self.sender()
        if "handData" not in globals():
            self.timer("Meting mislukt!")
            return
        if len(handData) != 0:
            data = handData
            self.timer("Meting geslaagd!")
            self.tabWidget.setTabEnabled(1,True)
        else:
            self.timer("Meting mislukt!")
            return
        img = Image.fromarray(cv.cvtColor(handImg, cv.COLOR_BGR2RGB))
        
        if name == 'duimView':
            data["hand_view"] = "thumb_side"
            self.handleData(name, data, img)
            self.nestedTabWidget.setTabEnabled(1,True)
            
        if name == 'pinkView':
            data["hand_view"] = "pink_side"
            self.handleData(name, data, img)
            self.nestedTabWidget.setTabEnabled(2,True)
            
            
        if name == 'vingerView':
            data["hand_view"] = "finger_side"
            self.handleData(name, data, img)
            self.nestedTabWidget.setTabEnabled(0,True)            
            
        if name == 'rugView':
            data["hand_view"] = "back_side"
            self.handleData(name, data, img)
            self.nestedTabWidget.setTabEnabled(3,True)
            
        
    def upload(self):
        status, s_id = sessionRequest(self.app.token_type, self.app.token, self.page.patient_id)
        if status == 'Ok':
            for key in self.resultaten.keys():
                status, res = uploadRequest(self.app.token_type, self.app.token, s_id, self.resultaten[key], self.imageNames[key])
                if status == 'Failed':
                    self.timer(res)
                    return
            self.closeMeting('upload')
        else:
            self.timer("Upload is mislukt!")
        
        
    def timer(self, text):
        if "geslaagd" in text or "created" in text:
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
        
    def closeStream(self):
        self.thread.exit()
        
    def closeMeting(self, text):
        self.page.patient_id = ''
        self.resultaten = {}
        self.imageNames = {}
        
        if text == 'back':
            self.setHidden()
            self.app.meting.select.getPatients()
            self.page.stackedWidget.setCurrentIndex(0)
            
        if text == 'upload':
            self.page.stackedWidget.setCurrentIndex(0)
            self.app.stackedWidget.setCurrentIndex(1)
            shutil.rmtree("temp")   
            
        if text == 'menu':
            self.setHidden()
            self.page.stackedWidget.setCurrentIndex(0)
            
        self.closeStream()
        self.thread.releaseCap()        
        
    def handleData(self, name, data, img):
        self.resultaten[name] = data
        path = f"temp/{name}.png"
            
        img.save(path, format="PNG")
        self.imageNames[name] = path
        
        colors = ["#ffe5b4", "#804080", "#ffcc00", "#30ff30", "#1565c0", '#ff3030']
        finger_thumb = pd.DataFrame(data['landmarks']['finger_thumb'])
        finger_index = pd.DataFrame(data['landmarks']['finger_index'])
        finger_middle = pd.DataFrame(data['landmarks']['finger_middle'])
        finger_ring = pd.DataFrame(data['landmarks']['finger_ring'])
        finger_pink = pd.DataFrame(data['landmarks']['finger_pink'])
        wrist = pd.DataFrame(data['landmarks']['wrist'])

        df = pd.concat([finger_thumb, finger_index, finger_middle, finger_ring, finger_pink, wrist], axis=1)
        model = PandasModel(df)
        
        # Omklappen zodat de X en Y coordinaten geinterpreteerd worden voor de plot
        df = df.T

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        padding = 50
        ax.axis([df['x'].min() - padding, df['x'].max() + padding, df['y'].min() - padding, df['y'].max() + padding])

        for k, v in df.iterrows():
            if "THUMB" in k:
                ax.scatter(v[0], v[1], color=colors[0])
            if "INDEX" in k:
                ax.scatter(v[0], v[1], color=colors[1])
            if "MIDDLE" in k:
                ax.scatter(v[0], v[1], color=colors[2])
            if "RING" in k:
                ax.scatter(v[0], v[1], color=colors[3])
            if "PINKY" in k:
                ax.scatter(v[0], v[1], color=colors[4])
            if "WRIST" in k:
                ax.scatter(v[0], v[1], color=colors[5])
                
            # ax.annotate(k, v,
            #             xytext=(-10,-10), 
            #             textcoords='offset points',
            #             size=4, 
            #             color='darkslategrey')
        ax.invert_yaxis()
        self.canvas = FigureCanvas(fig)
        toolbar = NavigationToolbar(self.canvas, self)
        
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(toolbar)
        plot_layout.addWidget(self.canvas)
        
        im2 = img.convert("RGBA")
        data = im2.tobytes("raw", "BGRA")
        qim = QImage(data, img.width, img.height, QImage.Format.Format_ARGB32)
        pixmap = QPixmap.fromImage(qim)    
                
        if name == 'duimView':
            if self.duim_visuals.itemAt(1):
                self.duim_visuals.itemAt(1).setParent(None)
            
            self.duimImage.setPixmap(pixmap)
            self.duim_visuals.addLayout(plot_layout)
            self.duimData.setModel(model)
            
            self.tabWidget.setCurrentIndex(1)
            self.nestedTabWidget.setCurrentIndex(1)
            
        if name == 'vingerView':
            if self.vinger_visuals.itemAt(1):
                self.vinger_visuals.itemAt(1).setParent(None)
            
            self.vingerImage.setPixmap(pixmap)
            self.vinger_visuals.addLayout(plot_layout)
            self.vingerData.setModel(model)
            
            self.tabWidget.setCurrentIndex(1)
            self.nestedTabWidget.setCurrentIndex(0)
            
        if name == 'pinkView':
            if self.pink_visuals.itemAt(1):
                self.pink_visuals.itemAt(1).setParent(None)
            
            self.pinkImage.setPixmap(pixmap)
            self.pink_visuals.addLayout(plot_layout)
            self.pinkData.setModel(model)
            
            self.tabWidget.setCurrentIndex(1)
            self.nestedTabWidget.setCurrentIndex(2)
            
        if name == 'rugView':
            if self.rug_visuals.itemAt(1):
                self.rug_visuals.itemAt(1).setParent(None)
            
            self.rugImage.setPixmap(pixmap)
            self.rug_visuals.addLayout(plot_layout)
            self.rugData.setModel(model)
            
            self.tabWidget.setCurrentIndex(1)
            self.nestedTabWidget.setCurrentIndex(3)
            
            
    @pyqtSlot(np.ndarray)
    def update_stream(self, img):
        """Updates the image_label with a new opencv image"""
        
        qt_img = self.convert_cv_qt(img)
        if qt_img:
            self.stream_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(convert_to_Qt_format) 