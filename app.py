from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget
from PyQt5 import uic, QtGui, QtCore
import sys

from pages.loginPage import LoginPage
from pages.homePage import HomePage
from pages.metingPage import MetingPage
from pages.resultatenPage import ResultatenPage

import os
import shutil

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.setWindowTitle("Handmetingen Tool")
        self.setWindowIcon(QtGui.QIcon("icons/app_icon.png"))
        self.setMinimumSize(1600 , 900)
        QtGui.QFontDatabase.addApplicationFont("styles/fonts/Humanist521LightBT.ttf")
        self.initUi()
        
        #Parameter storage
        self.token = ''
        self.token_type = '' 
        self.user = ''
    
    def closeEvent(self, event):
        if os.path.isdir("temp"):
            shutil.rmtree("temp")
        
    def initUi(self):
        self.stackedWidget = QStackedWidget()
        
        # Init widget
        self.login = LoginPage(self)
        self.home = HomePage(self)
        self.meting = MetingPage(self)
        self.resultaten = ResultatenPage(self)
        
        # Add to stack
        self.stackedWidget.addWidget(self.login)
        self.stackedWidget.addWidget(self.home)
        self.stackedWidget.addWidget(self.meting)
        self.stackedWidget.addWidget(self.resultaten)

        # Set all widgets
        self.setCentralWidget(self.stackedWidget)
        self.setStyleSheet(open('styles/index.css').read())
    
# Initialize the application
QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
app = QApplication(sys.argv)
AppWindow = App()
AppWindow.show()
app.exec()