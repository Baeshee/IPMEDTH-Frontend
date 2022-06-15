import shutil
from functools import partial

import cv2 as cv
import matplotlib
import numpy as np
from PIL import Image
from PyQt5 import Qt, uic
from PyQt5.QtCore import QThread, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QWidget

matplotlib.use("Qt5Agg")
import asyncio

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from handlers.createPlot import createPlot
from handlers.hand_detect_module import handDetect
from handlers.request_handlers import session_request, upload_request


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
        uic.loadUi("layout/metingComponent.ui", self)
        self.app = app
        self.page = page
        self.connectBtn()
        self.stream_label = self.videoLabel
        self.setHidden()

        self.resultaten = {}
        self.imageNames = {}

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_stream)

    def setHidden(self):
        self.toast.setHidden(True)
        self.tabWidget.setTabEnabled(1, False)
        for i in range(4):
            self.nestedTabWidget.setTabEnabled(i, False)

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
        self.closeMeting("back")

    def handleBtn(self, name):
        sender = self.sender()
        if "handData" not in globals():
            self.timer("Meting mislukt!")
            return
        if len(handData) != 0 and handData["hand_score"] > 0.8:
            data = handData
            self.timer("Meting geslaagd!")
            self.tabWidget.setTabEnabled(1, True)
        else:
            self.timer("Meting mislukt!")
            return
        img = Image.fromarray(cv.cvtColor(handImg, cv.COLOR_BGR2RGB))

        if name == "duimView":
            data["hand_view"] = "thumb_side"
            self.handleData(name, data, img)
            self.nestedTabWidget.setTabEnabled(1, True)

        if name == "pinkView":
            data["hand_view"] = "pink_side"
            self.handleData(name, data, img)
            self.nestedTabWidget.setTabEnabled(2, True)

        if name == "vingerView":
            data["hand_view"] = "finger_side"
            self.handleData(name, data, img)
            self.nestedTabWidget.setTabEnabled(0, True)

        if name == "rugView":
            data["hand_view"] = "back_side"
            self.handleData(name, data, img)
            self.nestedTabWidget.setTabEnabled(3, True)

    def upload(self):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(
            handleRequests(
                self.app,
                self.app.token_type,
                self.app.token,
                self.page.patient_id,
                self.resultaten,
                self.imageNames,
                self,
            )
        )
        self.closeMeting("upload")

    def timer(self, text):
        timer = QTimer(self)

        if timer.isActive():
            timer.stop()

        if "geslaagd" in text or "created" in text:
            self.toast.setStyleSheet("background-color: #2abd13;")
        else:
            self.toast.setStyleSheet("background-color: #bd1321;")

        self.toast.setText(text)
        self.toast.setHidden(False)

        timer.timeout.connect(self.setToHidden)
        timer.start(5000)

    def setToHidden(self):
        self.toast.setHidden(True)

    def closeStream(self):
        self.thread.exit()

    def closeMeting(self, text):
        self.page.patient_id = ""
        self.resultaten = {}
        self.imageNames = {}

        if text == "back":
            self.setHidden()
            self.app.measurement.select.get_patients()
            self.page.stacked_widget.setCurrentIndex(0)

        if text == "upload":
            self.page.stacked_widget.setCurrentIndex(0)
            self.app.stacked_widget.setCurrentIndex(1)

        if text == "menu":
            self.setHidden()
            self.page.stacked_widget.setCurrentIndex(0)

        self.closeStream()
        self.thread.releaseCap()

    def handleData(self, name, data, img):
        self.resultaten[name] = data
        path = f"temp/{name}.png"

        img.save(path, format="PNG")
        self.imageNames[name] = path

        fig, model = createPlot(data["landmarks"])

        self.canvas = FigureCanvas(fig)
        toolbar = NavigationToolbar(self.canvas, self)

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(toolbar)
        plot_layout.addWidget(self.canvas)

        im2 = img.convert("RGBA")
        data = im2.tobytes("raw", "BGRA")
        qim = QImage(data, img.width, img.height, QImage.Format.Format_ARGB32)
        pixmap = QPixmap.fromImage(qim)

        if name == "duimView":
            if self.duim_visuals.itemAt(1):
                self.duim_visuals.itemAt(1).setParent(None)

            self.duimImage.setPixmap(pixmap)
            self.duim_visuals.addLayout(plot_layout)
            self.duimData.setModel(model)

            self.tabWidget.setCurrentIndex(1)
            self.nestedTabWidget.setCurrentIndex(1)

        if name == "vingerView":
            if self.vinger_visuals.itemAt(1):
                self.vinger_visuals.itemAt(1).setParent(None)

            self.vingerImage.setPixmap(pixmap)
            self.vinger_visuals.addLayout(plot_layout)
            self.vingerData.setModel(model)

            self.tabWidget.setCurrentIndex(1)
            self.nestedTabWidget.setCurrentIndex(0)

        if name == "pinkView":
            if self.pink_visuals.itemAt(1):
                self.pink_visuals.itemAt(1).setParent(None)

            self.pinkImage.setPixmap(pixmap)
            self.pink_visuals.addLayout(plot_layout)
            self.pinkData.setModel(model)

            self.tabWidget.setCurrentIndex(1)
            self.nestedTabWidget.setCurrentIndex(2)

        if name == "rugView":
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
        convert_to_Qt_format = QImage(
            rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888
        )
        return QPixmap.fromImage(convert_to_Qt_format)


async def handleRequests(
    app, token_type, token, patient_id, resultaten, imageNames, main
):
    status, session_id = await asyncio.ensure_future(
        session_request(token_type, token, patient_id)
    )
    if status == "Ok":
        for key in resultaten.keys():
            status, res = await upload_request(
                token_type, token, session_id, resultaten[key], imageNames[key]
            )
            if status == "Failed":
                main.timer(res)
                return
        main.closeMeting("upload")
        app.home.main.timer(res)
    else:
        main.timer("Geen sessie aangemaakt!")
