from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class VingerComponent(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("component_ui/vinger_component.ui", self)


class DuimComponent(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("component_ui/duim_component.ui", self)


class PinkComponent(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("component_ui/pink_component.ui", self)


class RugComponent(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("component_ui/rug_component.ui", self)
