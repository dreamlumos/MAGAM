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
        self.setGeometry(200, 50, 1000, 650)
        self.setWindowTitle('MAGAM')

        self.system_state = system_state

        self.tabs = ResultsTabs(system_state, self)
        hbox = QHBoxLayout()
        hbox.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(hbox)
        container.setStyleSheet("QWidget#MWcontainer {background-color: #4F658A}")
        self.setCentralWidget(container)

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