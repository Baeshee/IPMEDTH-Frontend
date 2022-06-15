import asyncio
import json
from functools import partial

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import Qt, QtCore, QtWidgets, uic
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget

from components.sessieTable import SessieTable
from handlers.createPlot import createPlot
from handlers.requestHandlers import getImageRequest, getPatientRequest


class Main(QWidget):
    def __init__(self, app):
        super().__init__()
        uic.loadUi("layout/mainResultaten.ui", self)
        self.app = app
        self.sessieTable = SessieTable()
        self.setHidden()
        self.patient_data = []
        self.sessiesTabLayout.setContentsMargins(0, 0, 0, 0)
        self.pixmap = QPixmap()
        self.sessions = []
        self.measurements = []

        self.placeholder = QLabel("Deze patient heeft nog geen sessies")
        self.placeholder.setAlignment(Qt.Qt.AlignCenter)
        self.placeholder.setFont(QFont("Calibri", 24))
        self.patientNameField.textChanged.connect(self.on_search)

    def setHidden(self):
        self.detailTabWidget.setTabEnabled(1, False)
        for i in range(4):
            self.metingenTabWidget.setTabEnabled(i, False)

    def loadData(self):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        status, res = asyncio.run(getPatientRequest(self.app.token_type, self.app.token))
        if status == 'Ok':
            row = 0
            self.patientTable.setRowCount(len(res))
            for patient in res:
                self.patientTable.setItem(
                    row, 0, QtWidgets.QTableWidgetItem(str(patient["id"]))
                )
                self.patientTable.setItem(
                    row, 1, QtWidgets.QTableWidgetItem(patient["name"])
                )
                self.patientTable.setItem(
                    row, 2, QtWidgets.QTableWidgetItem(patient["email"])
                )
                self.patientTable.setItem(
                    row, 3, QtWidgets.QTableWidgetItem(str(len(patient["sessions"])))
                )
                self.patientTable.setItem(
                    row, 4, QtWidgets.QTableWidgetItem(patient["date_of_birth"])
                )
                row = row + 1

                self.patient_data.append(patient)
                self.connectEvents()
        else:
            print(res)

    def connectEvents(self):
        self.patientTable.doubleClicked.connect(self.set_sessions)

    def set_sessions(self):
        if self.sessiesTabLayout.itemAt(0):
            for i in range(self.sessiesTabLayout.count()):
                self.sessiesTabLayout.itemAt(i).widget().setParent(None)

        if len(self.patient_data[self.patientTable.currentRow()]["sessions"]) == 0:
            self.sessiesTabLayout.addWidget(self.placeholder)
        else:
            self.sessiesTabLayout.addWidget(self.sessieTable)
            row = 0
            self.sessieTable.table.setRowCount(
                len(self.patient_data[self.patientTable.currentRow()]["sessions"])
            )
            for session in self.patient_data[self.patientTable.currentRow()][
                "sessions"
            ]:
                self.sessieTable.table.setItem(
                    row, 0, QtWidgets.QTableWidgetItem(str(session["id"]))
                )
                self.sessieTable.table.setItem(
                    row,
                    1,
                    QtWidgets.QTableWidgetItem(str(len(session["measurements"]))),
                )
                self.sessieTable.table.setItem(
                    row, 2, QtWidgets.QTableWidgetItem(session["date"])
                )
                row = row + 1

        self.sessions = self.patient_data[self.patientTable.currentRow()]["sessions"]
        self.measurements = self.sessions[self.sessieTable.table.currentRow()][
            "measurements"
        ]
        self.sessieTable.table.doubleClicked.connect(self.set_measurements)

    def set_measurements(self):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        self.setHidden()
        first_tab = None

        for m in range(len(self.measurements)):
            m_data = self.measurements[m]
            data = {}
            data["finger_thumb"] = json.loads(m_data["finger_thumb"])
            data["finger_index"] = json.loads(m_data["finger_index"])
            data["finger_middle"] = json.loads(m_data["finger_middle"])
            data["finger_ring"] = json.loads(m_data["finger_ring"])
            data["finger_pink"] = json.loads(m_data["finger_pink"])
            data["wrist"] = json.loads(m_data["wrist"])

            fig, model = createPlot(data)
            self.canvas = FigureCanvas(fig)
            toolbar = NavigationToolbar(self.canvas, self)
            plot_layout = QVBoxLayout()
            plot_layout.addWidget(toolbar)
            plot_layout.addWidget(self.canvas)

            status, res = asyncio.run(
                getImageRequest(self.app.token_type, self.app.token, m_data["image"])
            )
            self.pixmap.loadFromData(res)

            if m_data["hand_view"] == "finger_side":
                if self.vingerPlot.itemAt(0):
                    self.vingerPlot.itemAt(0).setParent(None)

                self.vingerImage.setPixmap(self.pixmap)
                self.vingerPlot.addLayout(plot_layout)
                self.vingerTable.setModel(model)

                self.metingenTabWidget.setTabEnabled(0, True)
                if first_tab == None:
                    first_tab = 0

            elif m_data["hand_view"] == "thumb_side":
                if self.duimPlot.itemAt(0):
                    self.duimPlot.itemAt(0).setParent(None)

                self.duimImage.setPixmap(self.pixmap)
                self.duimPlot.addLayout(plot_layout)
                self.duimTable.setModel(model)

                self.metingenTabWidget.setTabEnabled(1, True)
                if first_tab == None:
                    first_tab = 1

            elif m_data["hand_view"] == "pink_side":
                if self.pinkPlot.itemAt(0):
                    self.pinkPlot.itemAt(0).setParent(None)

                self.pinkImage.setPixmap(self.pixmap)
                self.pinkPlot.addLayout(plot_layout)
                self.pinkTable.setModel(model)

                self.metingenTabWidget.setTabEnabled(2, True)
                if first_tab == None:
                    first_tab = 2

            elif m_data["hand_view"] == "back_side":
                if self.rugPlot.itemAt(0):
                    self.rugPlot.itemAt(0).setParent(None)

                self.rugImage.setPixmap(self.pixmap)
                self.rugPlot.addLayout(plot_layout)
                self.rugTable.setModel(model)

                self.metingenTabWidget.setTabEnabled(3, True)
                if first_tab == None:
                    first_tab = 3

        self.detailTabWidget.setCurrentIndex(1)
        self.metingenTabWidget.setCurrentIndex(first_tab)
        self.detailTabWidget.setTabEnabled(1, True)

    @QtCore.pyqtSlot()
    def on_search(self):
        text = self.patientNameField.text()
        for row in range(self.patientTable.rowCount()):
            item = self.patientTable.item(row, 1)
            if text:
                self.patientTable.setRowHidden(row, not self.filter(text, item.text()))
            else:
                self.patientTable.setRowHidden(row, False)

    def filter(self, text, keywords):
        return text.lower() in keywords.lower()
