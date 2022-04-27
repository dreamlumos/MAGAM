from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class PickUI(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # self.setGeometry(700, 250, 500, 400)

        layout = QHBoxLayout(self)

        self.debutant = QPushButton("Beginner", self)
        layout.addWidget(self.debutant, alignment=Qt.AlignLeft)

        self.expert = QPushButton("Expert", self)
        layout.addWidget(self.expert, alignment=Qt.AlignRight)

