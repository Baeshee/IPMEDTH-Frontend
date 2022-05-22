from PyQt6.QtWidgets import QMainWindow, QApplication, QStackedWidget
from PyQt6 import uic
import sys

from pages.loginPage import LoginPage
from pages.homePage import HomePage
from pages.metingPage import MetingPage

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.initUi()
        
        # Parameter storage
        self.token = ''
        self.token_type = ''
        self.user = ''
    
        
    def initUi(self):
        self.stackedWidget = QStackedWidget()
        
        # Init widget
        self.login = LoginPage(self)
        self.home = HomePage(self)
        self.meting = MetingPage(self)
        
        # Add to stack
        self.stackedWidget.addWidget(self.login)
        self.stackedWidget.addWidget(self.home)
        self.stackedWidget.addWidget(self.meting)

        # Set all widgets
        self.setCentralWidget(self.stackedWidget)
        self.setStyleSheet(open('styles/index.css').read())
    
# Initialize the application
app = QApplication(sys.argv)
AppWindow = App()
AppWindow.show()
app.exec()