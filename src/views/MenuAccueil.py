import ntpath

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from models.Aspect import *
from .BKT import *
from calculations import *


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


class MenuAccueil(QWidget):

    # A drop-down menu for aspects, M matrices, Q Matrices
    def __init__(self, remove, parent=None):
        QWidget.__init__(self, parent)
        self.remove = remove

        self.parent = parent
        self.setMinimumSize(100, 100)
        # self.setMaximumSize(200, 150)
        # self.setMaximumHeight(400)

        self.aspect_type = None
        if not (hasattr(self, "users_file")):
            self.users_file = None
        self.activities_file = None
        self.function = BasicFunctions.functions[0]  # by default for now

        layout = QVBoxLayout()

        remove_btn = QPushButton("-", self)
        # new_btn.setEnabled(False)
        remove_btn.setMaximumSize(35, 25)
        remove_btn.clicked.connect(lambda state, x=self: self.remove(x))
        layout.addWidget(remove_btn)

        # Aspect types dropdown menu
        label_aspect = QLabel("Aspect Type", self)
        label_aspect.setWordWrap(False)
        # label_aspect.setBuddy(self, )
        # label.setGeometry(500, 80, 280, 80)
        layout.addWidget(label_aspect)

        self.cb_aspect = QComboBox()
        self.cb_aspect.addItem("------")
        self.cb_aspect.addItems(Aspect.aspect_types)
        # Call aspect_change() if a new aspect type is selected in the drop-down menu
        self.cb_aspect.currentIndexChanged.connect(self.aspect_change)
        layout.addWidget(self.cb_aspect)

        self.pick_function = QComboBox()
        self.pick_function.currentIndexChanged.connect(self.function_picked)
        self.pick_function.addItems(BasicFunctions.functions)

        # M matrix dropdown menu
        label_users = QLabel("Upload M matrix (users)", self)
        label_users.setWordWrap(False)
        layout.addWidget(label_users)

        self.browse_btn = QRadioButton('Browse')
        self.create_btn = QRadioButton('Create Table')
        # self.browse_btn.toggled.connect(lambda: self.btnstate(self.browse_btn))
        # self.create_btn.toggled.connect(lambda: self.btnstate(self.create_btn))
        self.load_btn = QPushButton("Load")
        self.load_btn.clicked.connect(self.check_radio_btns)

        # self.browse_button_users = QPushButton("Browse...", self)
        # TODO here remove the file_name
        file_name = "C:/Users/zloui/PycharmProjects/MAGAM/data/motivation_users.csv"
        self.users_file = file_name
        self.browse_button_users = QPushButton("C:/Users/zloui/PycharmProjects/MAGAM/data/motivation_users.csv", self)
        self.browse_button_users.clicked.connect(self.load_users_file)
        layout.addWidget(self.browse_button_users)
        # Manually input the data
        self.create_users_table = QPushButton("Create Users Table")
        self.create_users_table.clicked.connect(self.create_users)
        layout.addWidget(self.create_users_table)
        # Create using BKT for aspect type didactic
        self.create_with_BKT = QPushButton("Create With BKT")
        self.create_with_BKT.setEnabled(False)
        self.create_with_BKT.clicked.connect(self.create_BKT)
        layout.addWidget(self.create_with_BKT)

        # Q matrix dropdown menu
        label_activities = QLabel("Upload Q matrix (activities)", self)
        layout.addWidget(label_activities)

        # self.browse_button_acts = QPushButton("Browse...", self)
        file_name = "C:/Users/zloui/PycharmProjects/MAGAM/data/motivation_activities.csv"
        self.activities_file = file_name
        self.browse_button_acts = QPushButton("C:/Users/zloui/PycharmProjects/MAGAM/data/motivation_activities.csv",
                                              self)
        self.browse_button_acts.clicked.connect(self.load_acts_file)
        layout.addWidget(self.browse_button_acts)
        # Manually input the data
        self.create_activities_table = QPushButton("Create Activities Table")
        self.create_activities_table.clicked.connect(self.create_acts)
        layout.addWidget(self.create_activities_table)

        layout.addWidget(QLabel("Function"))
        layout.addWidget(self.pick_function)

        self.setLayout(layout)
        # self.setWindowTitle("combo box demo")

        self.filled = False

    def check_radio_btns(self):
        if self.browse_btn.isChecked():
            self.load_users_file()
        if self.create_btn.isChecked():
            self.create_users()

    def function_picked(self):
        self.function = self.pick_function.currentText()
        print(self.function)

    # TODO: make it a pop-up window
    def create_users(self):
        print("You can now manually input the Users table")
        self.parent.parent.set_page_input_users(self)
        # TODO input file name into the browse button !!!
        print("created users input?")

    def create_acts(self):
        print("You can now manually input the Activities table")
        self.parent.parent.set_page_input_acts()

    def create_BKT(self):
        d = BKT(self)
        d.exec_()
        print(d.final_file)
        if d.final_file:
            self.users_file = d.final_file
            if len(d.final_file) == 0:
                self.browse_button_users.setText("Browse...")
            else:
                self.browse_button_users.setText(path_leaf(d.final_file))
        else:
            if self.users_file:
                self.browse_button_users.setText(path_leaf(self.users_file))

    def aspect_change(self):
        if self.cb_aspect.currentText() == "------":
            self.aspect_type = None
        else:
            self.aspect_type = self.cb_aspect.currentText()
            # Enable BKT for didactic aspect
            if self.aspect_type == Aspect.aspect_types[0]:
                self.create_with_BKT.setEnabled(True)
            else:
                self.create_with_BKT.setEnabled(False)
        self.check_filled()

    def load_users_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", "../data", "CSV (*.csv)")
        print(file_name)
        # TODO: in final version set QFileDialog open location as "./"
        # TODO: eventually "CSV (*.csv);; PKL (*.pkl);; JSON (*json)"
        print("here too:", self.users_file)
        if len(file_name[0]) > 0:
            self.users_file = file_name[0]
            self.browse_button_users.setText(path_leaf(file_name[0]))
        elif self.users_file:
            self.browse_button_users.setText(path_leaf(self.users_file))
        elif len(file_name[0]) == 0:
            self.browse_button_users.setText("Browse...")
        else:
            self.users_file = file_name[0]
            self.browse_button_users.setText(path_leaf(file_name[0]))
        self.check_filled()

    def load_acts_file(self):

        file_name = QFileDialog.getOpenFileName(self, "Open File", "../data", "CSV (*.csv)")
        # TODO: in final version set QFileDialog open location as "./"
        # TODO: eventually "CSV (*.csv);; PKL (*.pkl);; JSON (*json)"        self.activities_file = file_name[0]
        if len(file_name[0]) > 0:
            self.activities_file = file_name[0]
            self.browse_button_acts.setText(path_leaf(file_name[0]))
        elif self.activities_file:
            self.browse_button_users.setText(path_leaf(self.activities_file))
        elif len(file_name[0]) == 0:
            self.browse_button_acts.setText("Browse...")
        else:
            self.activities_file = file_name[0]
            self.browse_button_acts.setText(path_leaf(file_name[0]))
        self.check_filled()

    def check_filled(self):
        if self.aspect_type is None:
            self.filled = False
        elif self.users_file is None:
            self.filled = False
        elif self.activities_file is None:
            self.filled = False
        else:
            self.filled = True
        self.parent.check()

    def set_users_file(self, file):
        self.users_file = file
        print()
        print(file)
        print(self.users_file)
