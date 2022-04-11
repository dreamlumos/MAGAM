from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .WelcomeScreen import *
from .PickUI import *
from .Aspects import *
from .Sorry import *
from .Results import *


class MainWindow(QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # self.resize(600, 500)

        # Create stack and horizontal layout
        self.Stack = QStackedWidget()
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.Stack)

        # Add Welcome widget and object
        self.welcome = WelcomeScreen(self)
        self.Stack.addWidget(self.welcome)
        # Connect welcome button to next page
        self.welcome.welcome_btn.clicked.connect(self.set_page_pick)

        # Add PickUI widget and object
        self.pick = PickUI(self)
        self.Stack.addWidget(self.pick)
        # Connect buttons to switch pages
        self.pick.debutant.clicked.connect(self.set_page_calcul)
        self.pick.expert.clicked.connect(self.set_page_sorry)

        # Add Aspects widget and object
        self.asp = Aspects(self)
        self.Stack.addWidget(self.asp)

        # Add SorryPage widget and object
        self.sorry_page = SorryPage(self)
        self.Stack.addWidget(self.sorry_page)
        # Connect back button to Pick page
        self.sorry_page.back.clicked.connect(self.set_page_pick)

        self.setGeometry(700, 250, 500, 400)
        self.setWindowTitle('Interface demo')

    def next_page(self):
        new_index = self.Stack.currentIndex() + 1
        if new_index < len(self.Stack):
            self.display(new_index)

    def prev_page(self):
        new_index = self.Stack.currentIndex() - 1
        if new_index >= 0:
            self.display(new_index)

    def set_page_sorry(self):
        self.display(3)
        self.setWindowTitle("Sorry!")

    def set_page_pick(self):
        self.display(1)
        self.setWindowTitle("pick an UI")

    def set_page_calcul(self):
        self.display(2)
        self.setWindowTitle("Calcul des recommandations d'activités")

    def display(self, i):
        self.Stack.setCurrentIndex(i)