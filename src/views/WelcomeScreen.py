from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class WelcomeScreen(QWidget):
    def __init__(self, parent=None):
        super(WelcomeScreen, self).__init__(parent)
        # self.setGeometry(700, 250, 500, 400)
        
        layout = QGridLayout(self)

        labelHello = QLabel("Hello!")
        layout.addWidget(labelHello, 0, 1)

        # Create welcome button
        self.welcome_btn = QPushButton("Welcome", self)

        # Tried some CSS real quick
        # self.welcome_btn.setStyleSheet(
        #     "*{border: 4px solid '#ADD8E6';" +
        #     "border-radius: 15px;" +
        #     "font-size: 25px;" +
        #     # "margin: 100px 200px;" +
        #     "padding: 25 10;}" +
        #     "*:hover{background-color: '#ADD8E6';" +
        #     "color: 'white'}"
        #     # +
        #     # "*block:hover{margin: 0 0;}"
        #     # +
        #     # "*block:hover{margin:0px;}"
        # )

        # Adding the welcome button to the widget
        layout.addWidget(self.welcome_btn, 1, 1)
