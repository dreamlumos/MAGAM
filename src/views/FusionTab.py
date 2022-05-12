import datetime
import os

import PyQt5.QtBluetooth
import pandas
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from fusion import FusionFunctions
import numpy as np

import ntpath

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


class FusionTab(QWidget):

    def __init__(self, controller, parent=None):
        # Recommendations as seen from the selection side, ie which activity for which student
        super(FusionTab, self).__init__(parent)

        self.controller = controller
        self.layout = QHBoxLayout(self)
        self.tables = []  # list of the tables we want to fusion

        self.calculate_btn = QPushButton("Calculate")
        self.calculate_btn.setEnabled(False)

        self.add_btn = QPushButton(" + ")
        self.remove_btn = QPushButton(" - ")

        self.add_btn.setToolTip("Add a table to fusion with the precedent.")
        self.add_btn.clicked.connect(self.add_table)

        self.remove_btn.setToolTip("Remove the table and its associated fusion's function.")
        # self.remove_btn.clicked.connect(self.remove_table)

        self.add_table()

        self.setLayout(self.layout)

    def add_table(self):
        l = len(self.tables)
        new_table = QPushButton("Browse...")
        new_table.clicked.connect(lambda state, x=new_table: self.load_file(x))
        self.tables.append(new_table)

        curr = len(self.tables)
        self.calculate_btn.setEnabled(curr > 1)
        self.layout.addWidget(self.tables[-1])
        self.layout.addWidget(self.add_btn)
        self.layout.addWidget(self.remove_btn)
        self.layout.addWidget(self.calculate_btn)
        # self.layout.addWidget(self.add_aspect_btn)

    def remove_table(self, widg):
        # Remove the aspect from the display
        self.layout.removeWidget(widg)
        # self.layout.removeWidget(self.remove_btns[i])
        # Remove the aspect from the list
        place = self.tables.index(widg)
        self.tables.remove(widg)
        for k in range(place, len(self.tables)):
            # print(self.drop_menu_list[k])
            self.layout.addWidget(self.tables[k])
        self.layout.addWidget(self.add_btn)
        self.layout.addWidget(self.remove_btn)
        self.layout.addWidget(self.calculate_btn)
        # self.pick_fusion.setEnabled(l > 1)
        widg.deleteLater()
        # self.check()

    def load_file(self, btn):
        file_name = QFileDialog.getOpenFileName(self, "Open File", "../data", "CSV (*.csv)")
        if len(file_name[0]) > 0:
            btn.setText(path_leaf(file_name[0]))
        elif len(file_name[0]) == 0:
            btn.setText("Browse...")