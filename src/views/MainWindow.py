from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .WelcomeScreen import *
from .PickUI import *
from .Aspects import *
from .Result import *
from .ResultsTabs import *
from .InputUsers import *
from .InputActs import *
from .Sorry import *

class MainWindow(QMainWindow):

    def __init__(self, system_state, parent=None):
        super(MainWindow, self).__init__(parent)
        # self.resize(600, 500)

        self.system_state = system_state

        # Create stack and horizontal layout
        self.Stack = QStackedWidget()
        hbox = QHBoxLayout()
        hbox.addWidget(self.Stack)

        # Add Welcome widget and object
        WelcomeScreen_widget = WelcomeScreen(self)
        # WelcomeScreen_widget.welcome_btn.clicked.connect(self.set_page_pick)
        WelcomeScreen_widget.welcome_btn.clicked.connect(self.set_page_aspects)
        self.WelcomeScreen_index = self.Stack.addWidget(WelcomeScreen_widget)

        self.setGeometry(200, 50, 1000, 650)
        self.setWindowTitle('MAGAM')

        container = QWidget()
        container.setLayout(hbox)
        container.setStyleSheet("QWidget#MWcontainer {background-color: #4F658A}")
        self.setCentralWidget(container)

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
            PickUI_widget.debutant.clicked.connect(self.set_page_aspects) # move to PickUI ?
            # PickUI_widget.debutant.clicked.connect(self.set_page_data_manually) # move to PickUI ?
            PickUI_widget.expert.clicked.connect(self.set_page_sorry) # move to PickUI ?
            self.PickUI_index = self.Stack.addWidget(PickUI_widget)

        self.display(self.PickUI_index)
        self.setWindowTitle("Pick an UI")

    def set_page_aspects(self):
        if not(hasattr(self, 'Input_index')):
            Aspects_widget = Aspects(self.system_state, self)
            self.Input_index = self.Stack.addWidget(Aspects_widget)

        self.display(self.Input_index)
        self.setWindowTitle("Input aspects")

    def set_page_input_users(self, drop_menu):
        if not(hasattr(self, 'Input_Users')):
            data_input_widget = InputUsers(self, drop_menu)
            data_input_widget.ok_btn.clicked.connect(lambda state, x=data_input_widget: self.delete_input_users(x))
            data_input_widget.cancel_btn.clicked.connect(self.set_page_aspects)
            self.Input_Users = self.Stack.addWidget(data_input_widget)

        self.display(self.Input_Users)
        self.setWindowTitle("Manually input your users data")

    def delete_input_users(self, widg):
        if hasattr(self, 'Input_Users'):
            file_name = widg.drop_menu.users_file
            widg.deleteLater()
            delattr(self, 'Input_Users')
            print(hasattr(self, 'Input_Users'))
            self.set_page_aspects()

    def set_page_input_acts(self):
        if not(hasattr(self, 'Input_Acts')):
            data_input_widget = InputActs(self)
            data_input_widget.ok_btn.clicked.connect(lambda state, x=data_input_widget: self.delete_input_acts(x))
            data_input_widget.cancel_btn.clicked.connect(self.set_page_aspects)
            self.Input_Acts = self.Stack.addWidget(data_input_widget)

        self.display(self.Input_Acts)
        self.setWindowTitle("Manually input your activities data")

    def delete_input_acts(self, widg):
        if hasattr(self, 'Input_Acts'):
            widg.deleteLater()
            delattr(self, 'Input_Acts')
            print(hasattr(self, 'Input_Acts'))
            self.set_page_aspects()

    # def set_page_results(self):
    #     if not(hasattr(self, 'Results_index')):
    #         Results_widget = Result(self.system_state, self)
    #         self.Results_index = self.Stack.addWidget(Results_widget)
    #
    #     self.display(self.Results_index)
    #     self.setWindowTitle("Result")

    def set_page_results(self):
        if not(hasattr(self, 'Results_index')):
            Results_widget = ResultsTabs(self.system_state, self)
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