"""Main measurement component."""

import asyncio
from functools import partial

import cv2
import matplotlib
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PIL import Image
from PyQt5 import uic
from PyQt5.QtCore import QThread, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from handlers.createPlot import createPlot
from handlers.hand_detect_module import handDetect
from handlers.request_handlers import session_request, upload_request

matplotlib.use("Qt5Agg")


class VideoThread(QThread):
    """VideoThread class."""

    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.detector = handDetect(detectCon=0.8, maxHands=2)
        self.stop = False
        self.cap = None

    def run(self):
        """Run video thread."""
        self.cap = cv2.VideoCapture(0)
        while True:
            ret, img = self.cap.read()
            hands, img = self.detector.staticImage(img)
            global handData
            handData = hands

            global handImg
            handImg = img

            if ret:
                self.change_pixmap_signal.emit(img)

            if self.stop is True:
                break

    def release_cap(self):
        """Release video capture."""
        if self.cap is not None:
            self.stop = True
            self.cap.release()
            self.stop = False
        else:
            return


class Main(QWidget):
    """Menu QWidget class."""

    def __init__(self, app, page):
        super().__init__()
        uic.loadUi("layout/metingComponent.ui", self)
        self.app = app
        self.page = page
        self.connect_btn()
        self.stream_label = self.videoLabel
        self.set_hidden()

        self.results = {}
        self.image_names = {}

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_stream)

    def set_hidden(self):
        """Set all tabs to hidden."""
        self.toast.setHidden(True)
        self.tabWidget.setTabEnabled(1, False)
        for i in range(4):
            self.nestedTabWidget.setTabEnabled(i, False)

    def connect_btn(self):
        """Connect buttons to functions."""
        buttons = [
            self.duimView,
            self.pinkView,
            self.vingerView,
            self.rugView,
        ]

        for btn in buttons:
            btn.clicked.connect(partial(self.handle_btn, btn.objectName()))

        # Isolated calls
        self.backBtn.clicked.connect(self.back)
        self.uploadBtn.clicked.connect(self.upload)

    def back(self):
        """Close stream and go back."""
        self.close_measurement("back")

    def handle_btn(self, name):
        """Handle button clicks."""
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
        img = Image.fromarray(cv2.cvtColor(handImg, cv2.COLOR_BGR2RGB))

        if name == "duimView":
            data["hand_view"] = "thumb_side"
            self.handle_data(name, data, img)
            self.nestedTabWidget.setTabEnabled(1, True)

        if name == "pinkView":
            data["hand_view"] = "pink_side"
            self.handle_data(name, data, img)
            self.nestedTabWidget.setTabEnabled(2, True)

        if name == "vingerView":
            data["hand_view"] = "finger_side"
            self.handle_data(name, data, img)
            self.nestedTabWidget.setTabEnabled(0, True)

        if name == "rugView":
            data["hand_view"] = "back_side"
            self.handle_data(name, data, img)
            self.nestedTabWidget.setTabEnabled(3, True)

    def upload(self):
        """Upload data to API."""
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(
            handle_requests(
                self.app,
                self.app.token_type,
                self.app.token,
                self.page.patient_id,
                self.results,
                self.image_names,
                self,
            )
        )
        self.close_measurement("upload")

    def timer(self, text):
        """Show toast message and set timer."""
        timer = QTimer(self)

        if timer.isActive():
            timer.stop()

        if "geslaagd" in text or "created" in text:
            self.toast.setStyleSheet("background-color: #2abd13;")
        else:
            self.toast.setStyleSheet("background-color: #bd1321;")

        self.toast.setText(text)
        self.toast.setHidden(False)

        timer.timeout.connect(self.set_to_hidden)
        timer.start(5000)

    def set_to_hidden(self):
        """Set toast to hidden."""
        self.toast.setHidden(True)

    def close_stream(self):
        """Close stream thread."""
        self.thread.exit()

    def close_measurement(self, text):
        """Close measurement and go back."""
        self.page.patient_id = ""
        self.results = {}
        self.image_names = {}

        if text == "back":
            self.set_hidden()
            self.app.measurement.select.get_patients()
            self.page.stacked_widget.setCurrentIndex(0)

        if text == "upload":
            self.page.stacked_widget.setCurrentIndex(0)
            self.app.stacked_widget.setCurrentIndex(1)

        if text == "menu":
            self.set_hidden()
            self.page.stacked_widget.setCurrentIndex(0)

        self.close_stream()
        self.thread.release_cap()

    def handle_data(self, name, data, img):
        """Handle data."""
        self.results[name] = data
        path = f"temp/{name}.png"

        img.save(path, format="PNG")
        self.image_names[name] = path

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

        if qt_img := self.convert_cv_qt(img):
            self.stream_label.setPixmap(qt_img)

    def convert_cv_qt(self, img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(
            rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888
        )
        return QPixmap.fromImage(convert_to_qt_format)


async def handle_requests(
    app, token_type, token, patient_id, results, image_names, main
):
    """Handle requests."""
    status, session_id = await asyncio.ensure_future(
        session_request(token_type, token, patient_id)
    )
    if status == "Ok":
        for key in results.keys():
            status, res = await upload_request(
                token_type, token, session_id, results[key], image_names[key]
            )
            if status == "Failed":
                main.timer(res)
                return
        main.close_measurement("upload")
        app.home.main.timer(res)
    else:
        main.timer("Geen sessie aangemaakt!")
