from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from models.Aspect import *
import ntpath

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

class DropMenu(QWidget):

    # A drop-down menu for aspects, M matrices, Q Matrices
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(700, 250, 500, 400)

        self.parent = parent
        self.setMinimumSize(100, 100)
        # self.setMaximumSize(200, 150)
        # self.setMaximumHeight(400)

        self.aspect_type = None 
        self.users_file = None
        self.activities_file = None

        layout = QVBoxLayout()

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

        # M matrix dropdown menu
        label_users = QLabel("Upload M matrix (users)", self)
        label_users.setWordWrap(False)
        layout.addWidget(label_users)

        self.browse_button_users = QPushButton("Browse...", self)
        self.browse_button_users.clicked.connect(self.load_users_file)
        layout.addWidget(self.browse_button_users)

        # Q matrix dropdown menu
        label_activities = QLabel("Upload Q matrix (activities)", self)
        layout.addWidget(label_activities)

        self.browse_button_acts = QPushButton("Browse...", self)
        self.browse_button_acts.clicked.connect(self.load_acts_file)
        layout.addWidget(self.browse_button_acts)

        self.setLayout(layout)
        # self.setWindowTitle("combo box demo")

        self.filled = False

    def aspect_change(self):
        if self.cb_aspect.currentText() == "------":
            self.aspect_type = None
        else:
            self.aspect_type = self.cb_aspect.currentText()
        self.check_filled()

    def load_users_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", "./", "CSV (*.csv)")
        # eventually "CSV (*.csv);; PKL (*.pkl);; JSON (*json)"
        self.users_file = file_name[0]
        if len(file_name[0]) == 0:
            self.browse_button_users.setText("Browse...")
        else:
            self.browse_button_users.setText(path_leaf(file_name[0]))
        self.check_filled()

    def load_acts_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", "./", "CSV (*.csv)")
        # eventually "CSV (*.csv);; PKL (*.pkl);; JSON (*json)"
        self.activities_file = file_name[0]
        if len(file_name[0]) == 0:
            self.browse_button_acts.setText("Browse...")
        else:
            self.browse_button_acts.setText(path_leaf(file_name[0]))
        self.check_filled()

    def check_filled(self):
        if self.aspect_type == None:
            self.filled = False
        elif self.users_file == None:
            self.filled = False
        elif self.activities_file == None:
            self.filled = False
        else: 
            self.filled = True
        self.parent.check()