from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from models.Aspect import *
from calculations import *
from .AspectTab import *
from .Aspects import *
from .BKT import *

import ntpath

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

class DropMenu(QWidget):

    # A drop-down menu for aspects, M matrices, Q Matrices
    def __init__(self, controller, aspect_id, remove, parent=None):
        super().__init__(parent)

        self.controller = controller
        self.remove = remove
        self.parent = parent
        self.setMinimumSize(100, 100)

        self.aspect_id = aspect_id
        self.aspect_type = None

        if not(hasattr(self, "users_file")):
            self.users_file = None

        self.activities_file = None

        self.function = None

        layout = QVBoxLayout()

        remove_btn = QPushButton("-", self)
        remove_btn.setMaximumSize(40, 40)
        # remove_btn.setFixedSize(35, 25)
        # remove_btn.setStyleSheet(
        #     "*{width: 35;}")
        remove_btn.clicked.connect(lambda state, x=self: self.remove(x))
        layout.addWidget(remove_btn)

        # Aspect types dropdown menu
        label_aspect = QLabel("Aspect type", self)
        label_aspect.setWordWrap(False)
        layout.addWidget(label_aspect)

        self.cb_aspect = QComboBox()
        # self.cb_aspect.setPlaceholderText("")
        self.cb_aspect.addItems(Aspect.aspect_types)
        self.aspect_type = self.cb_aspect.currentText()
        self.cb_aspect.currentIndexChanged.connect(self.aspect_change)
        layout.addWidget(self.cb_aspect)

        # M matrix dropdown menu
        label_users = QLabel("Upload M matrix (users)", self)
        label_users.setWordWrap(False)
        layout.addWidget(label_users)

        self.browse_button_users = QPushButton("Browse Files...", self)
        self.browse_button_users.clicked.connect(self.load_users_file)
        layout.addWidget(self.browse_button_users)

        self.create_with_BKT = QPushButton("Create With BKT")
        self.create_with_BKT.setToolTip("BKT is used to infer students’ mastery of specific knowledge components.\nIt requires a specific CSV formatting.\nPlease refer to the User Manual for more details.")
        self.create_with_BKT.setEnabled(False)
        self.create_with_BKT.clicked.connect(self.create_BKT)
        layout.addWidget(self.create_with_BKT)

        # Q matrix dropdown menu
        label_activities = QLabel("Upload Q matrix (activities)", self)
        layout.addWidget(label_activities)

        self.browse_button_acts = QPushButton("Browse Files...", self)
        self.browse_button_acts.clicked.connect(self.load_acts_file)
        layout.addWidget(self.browse_button_acts)

        layout.addWidget(QLabel("Function"))
        self.pick_function = QComboBox()
        self.pick_function.currentIndexChanged.connect(self.function_picked)
        self.pick_function.addItems(basic_functions)
        layout.addWidget(self.pick_function)

        self.calculate_btn = QPushButton("Calculate recommendations")
        self.calculate_btn.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_btn)

        self.setLayout(layout)

        self.check_filled()

    def calculate(self):
        try:
            users_qtable, act_qtable, rec_qtable = self.controller.update_aspect_from_files(self.aspect_id, self.aspect_type, self.users_file, self.activities_file, self.function)
        except ValueError as e:
            msg = QMessageBox()
            msg.setText("Error")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            self.parent.parent.add_page(self.aspect_type, users_qtable, act_qtable, rec_qtable, self.function)

    def function_picked(self):
        self.function = self.pick_function.currentText()

    def create_BKT(self):
        d = BKT(self)
        d.exec_()
        print(d.final_file)
        if d.final_file:
            self.users_file = d.final_file
            if len(d.final_file) == 0:
                self.browse_button_users.setText("Browse Files...")
            else:
                self.browse_button_users.setText(path_leaf(d.final_file))
        else:
            if self.users_file:
                self.browse_button_users.setText(path_leaf(self.users_file))
            else:
                self.browse_button_users.setText("Browse Files...")

    def aspect_change(self):
        self.aspect_type = self.cb_aspect.currentText()
        # Enable BKT for didactic aspect
        if self.aspect_type == Aspect.aspect_types[1]:  # Didactic aspect
            self.create_with_BKT.setEnabled(True)
        else:
            self.create_with_BKT.setEnabled(False)
        self.check_filled()

    def load_users_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", "../data", "CSV (*.csv)")
        # TODO: in final version set QFileDialog open location as "./"
        # TODO: eventually "CSV (*.csv);; PKL (*.pkl);; JSON (*json)"
        # print("here too:", self.users_file)
        if len(file_name[0]) > 0:  # chosen file has a name
            self.users_file = file_name[0]
            self.browse_button_users.setText(path_leaf(file_name[0]))
        elif self.users_file:  # if the user clicked on browse but didn't select a file, keep previous file name
            self.browse_button_users.setText(path_leaf(self.users_file))
        elif len(file_name[0]) == 0:
            self.browse_button_users.setText("Browse Files...")

        self.check_filled()

    def load_acts_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", "../data", "CSV (*.csv)")
        # TODO: in final version set QFileDialog open location as "./"
        # TODO: eventually "CSV (*.csv);; PKL (*.pkl);; JSON (*json)"        self.activities_file = file_name[0]
        if len(file_name[0]) > 0:  # chosen file has a name
            self.activities_file = file_name[0]
            self.browse_button_acts.setText(path_leaf(self.activities_file))
        elif self.activities_file:  # if the user clicked on browse but didn't select a file, keep previous file name
            self.browse_button_users.setText(path_leaf(self.activities_file))
        elif len(file_name[0]) == 0:
            self.browse_button_acts.setText("Browse Files...")

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

        if self.filled == False:
            self.calculate_btn.setEnabled(False)
        else: 
            self.calculate_btn.setEnabled(True)
