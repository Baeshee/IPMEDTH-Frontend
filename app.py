from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QWidget, QFrame, QTextEdit, QStackedWidget, QHBoxLayout
from PyQt6 import uic
import sys
from functools import partial

from pages.homePage import HomePage
from pages.metingPage import MetingPage

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.initUi()
        self.connectBtn()
        
    def initUi(self):
        self.stackedWidget = QStackedWidget()
        
        # Init widget
        self.home = HomePage()
        self.meting = MetingPage()
        
        # Add to stack
        self.stackedWidget.addWidget(self.home)
        self.stackedWidget.addWidget(self.meting)

        # Set all widgets
        self.setCentralWidget(self.stackedWidget)
        

    def connectBtn(self):    
        buttons = [
            self.home.menu.homeBtn,
            self.meting.menu.homeBtn,
            self.home.menu.metingBtn,
            self.meting.menu.metingBtn,
            self.home.menu.resultatenBtn,
            self.meting.menu.resultatenBtn
        ]
        
        for btn in buttons:
            btn.clicked.connect(partial(self.handle_btn, btn.text()))
        
    def handle_btn(self, name):
        if name == 'Home':
            self.stackedWidget.setCurrentIndex(0)
        elif name == 'Meting':
            self.stackedWidget.setCurrentIndex(1)
        elif name == 'Resultaten':
            self.stackedWidget.setCurrentIndex(2)
        
# Initialize the application
app = QApplication(sys.argv)
AppWindow = App()
AppWindow.show()
app.exec()