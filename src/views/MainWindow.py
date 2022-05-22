from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .TabContainer import *


class MainWindow(QMainWindow):

    def __init__(self, controller, parent=None):
        super().__init__(parent)

        self.setGeometry(200, 50, 1000, 650)
        self.setWindowTitle('MAGAM')

        self.controller = controller

        self.tabs = TabContainer(controller, self)
        hbox = QHBoxLayout()
        hbox.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(hbox)
        container.setStyleSheet("QWidget#MWcontainer {background-color: #4F658A}")
        self.setCentralWidget(container)
