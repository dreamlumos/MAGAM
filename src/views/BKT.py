from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from models.BKTData import *

import ntpath


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


class BKT(QDialog):

    def __init__(self, parent=None):
        super(BKT, self).__init__(parent)

        self.users_file = None
        self.final_file = None
        self.setWindowTitle("Create a table using BKT")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        # QBtn.Ok.setEnabled(False)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.accepted.connect(self.calculate_BKT)
        # self.buttonBox.accepted.connect(self.ac)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Choose a file to be processes using BKT.")
        self.layout.addWidget(message)

        self.browse_button_users = QPushButton("Browse...", self)
        self.browse_button_users.clicked.connect(self.load_users_file)
        self.layout.addWidget(self.browse_button_users)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def load_users_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", "../data", "CSV (*.csv)")
        # TODO: in final version set QFileDialog open location as "./"
        # TODO: eventually "CSV (*.csv);; PKL (*.pkl);; JSON (*json)"
        self.users_file = file_name[0]
        print("users file:", self.users_file)
        if len(file_name[0]) == 0:
            self.browse_button_users.setText("Browse...")
        else:
            self.browse_button_users.setText(path_leaf(file_name[0]))
            # self.buttonBox.accepted.setEnabled(True)
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    def calculate_BKT(self):
        print("calculating bkt")
        d = BKTData(self.users_file)  # {'User': 'user_id', 'KC': 'skill_name', 'IsCorrect': 'correct'}
        print("bkt created")
        self.final_file = d.save_preds_to_csv()
        # d.deleteLater()
        # del d
        self.accept()
