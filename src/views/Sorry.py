from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class SorryPage(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        layout = QHBoxLayout(self)

        sorry = QLabel("Sorry! This page has not yet been implemented! Please come back later.")
        sorry.setWordWrap(True)
        layout.addWidget(sorry)

        self.back = QPushButton("Back", self)
        layout.addWidget(self.back)
