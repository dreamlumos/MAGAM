from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .WelcomeScreen import *
from .PickUI import *
from .Aspects import *
from .Results import *
from .Sorry import *

class MainWindow(QWidget):

    def __init__(self, system_state, parent=None):
        super(MainWindow, self).__init__(parent)
        # self.resize(600, 500)

        self.system_state = system_state

        # Create stack and horizontal layout
        self.Stack = QStackedWidget()
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.Stack)

        # Add Welcome widget and object
        WelcomeScreen_widget = WelcomeScreen(self)
        WelcomeScreen_widget.welcome_btn.clicked.connect(self.set_page_pick)
        self.WelcomeScreen_index = self.Stack.addWidget(WelcomeScreen_widget)

        self.setGeometry(700, 250, 500, 400)
        self.setWindowTitle('MAGAM')

    # Unused for the moment : 

    # def next_page(self):
    #     new_index = self.Stack.currentIndex() + 1
    #     if new_index < len(self.Stack):
    #         self.display(new_index)

    # def prev_page(self):
    #     new_index = self.Stack.currentIndex() - 1
    #     if new_index >= 0:
    #         self.display(new_index)

    def set_page_pick(self):

        if not(hasattr(self, 'PickUI_index')):
            PickUI_widget = PickUI(self)
            PickUI_widget.debutant.clicked.connect(self.set_page_input) # move to PickUI ?
            PickUI_widget.expert.clicked.connect(self.set_page_sorry) # move to PickUI ?
            self.PickUI_index = self.Stack.addWidget(PickUI_widget)

        self.display(self.PickUI_index)
        self.setWindowTitle("Pick an UI")

    def set_page_input(self):

        if not(hasattr(self, 'Input_index')):
            Aspects_widget = Aspects(self.system_state, self)
            self.Input_index = self.Stack.addWidget(Aspects_widget)

        self.display(self.Input_index)
        self.setWindowTitle("Input aspects")

    def set_page_results(self):
        if not(hasattr(self, 'Results_index')):
            Results_widget = Results(self.system_state, self)
            self.Results_index = self.Stack.addWidget(Results_widget)

        self.display(self.Results_index)
        self.setWindowTitle("Results")

    def set_page_sorry(self):

        if not(hasattr(self, 'Results_index')):
            Sorry_widget = Sorry(self)
            Sorry_widget.back.clicked.connect(self.set_page_pick)
            self.Sorry_index = self.Stack.addWidget(Sorry_widget)

        self.display(self.Sorry_index)
        self.setWindowTitle("Sorry!")

    def display(self, i):
        self.Stack.setCurrentIndex(i)