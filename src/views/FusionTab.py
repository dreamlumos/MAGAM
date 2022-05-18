import datetime
import os

import PyQt5.QtBluetooth
import pandas
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from fusion import *
import numpy as np

import ntpath

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


class FusionTab(QWidget):

    def __init__(self, controller, recommendations_qtable=None, function=None, parent=None):
        super().__init__(parent)

        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        self.controller = controller
        self.parent = parent

        self.function = function
        self.aspect_1 = None
        self.aspect_2 = None

        self.combo_list = self.get_ID()

        top_widget = QWidget()
        t_layout = QHBoxLayout()
        self.table_1 = QComboBox()
        self.table_1.setPlaceholderText("NO")
        self.table_1.addItems(self.combo_list)
        self.table_1.currentIndexChanged.connect(self.set_aspect_1)
        t_layout.addWidget(self.table_1)

        self.fusion_func = QComboBox()
        self.fusion_func.addItems(fusion_functions)
        self.function = self.fusion_func.currentText()
        self.fusion_func.currentIndexChanged.connect(self.set_function)
        t_layout.addWidget(self.fusion_func)

        self.table_2 = QComboBox()
        self.table_2.setPlaceholderText("NO")
        self.table_2.addItems(self.combo_list)
        self.table_2.currentIndexChanged.connect(self.set_aspect_2)
        t_layout.addWidget(self.table_2)

        self.calc = QPushButton("Calculate")
        self.calc.clicked.connect(self.calculate)
        self.calc.setEnabled(False)
        t_layout.addWidget(self.calc)

        top_widget.setLayout(t_layout)

        self.layout.addWidget(top_widget, 0, 0)

        bottom_widget = QWidget()
        b_layout = QHBoxLayout()
        self.table_widget = QTableWidget(50, 50, self)
        self.table_widget.resizeColumnsToContents()
        b_layout.addWidget(self.table_widget)
        bottom_widget.setLayout(b_layout)

        top_label = QLabel("Fusion table")
        b_layout.addWidget(top_label)
        # b_layout.addStretch(1)

        save_as_csv_button = QPushButton("Save As...")
        save_as_csv_button.setToolTip("Save the fusion table as a CSV file.")  # TODO: eventually add other file types
        save_as_csv_button.clicked.connect(lambda state, qtable=self.table_widget: self.controller.save_as_csv(self, qtable))
        b_layout.addWidget(save_as_csv_button)

        self.layout.addWidget(bottom_widget, 1, 0)


        # self.buttons_widget = self._create_buttons_widget(aspect_type, function)

    # def __init__(self, controller, parent=None):
    #     # Recommendations as seen from the selection side, ie which activity for which student
    #     super(FusionTab, self).__init__(parent)
    #
    #     self.controller = controller
    #     self.layout = QHBoxLayout(self)
    #     self.tables = []  # list of the tables we want to fusion
    #
    #     self.calculate_btn = QPushButton("Calculate")
    #     self.calculate_btn.setEnabled(False)
    #
    #     self.add_btn = QPushButton(" + ")
    #     self.remove_btn = QPushButton(" - ")
    #
    #     self.add_btn.setToolTip("Add a table to fusion with the precedent.")
    #     # self.add_btn.clicked.connect(self.add_table)
    #
    #     self.remove_btn.setToolTip("Remove the table and its associated fusion's function.")
    #     # self.remove_btn.clicked.connect(self.remove_table)
    #
    #     self.add_table()
    #
    #     self.setLayout(self.layout)

    # def add_table(self):
    #     l = len(self.tables)
    #     new_table = QPushButton("Browse...")
    #     new_table.clicked.connect(lambda state, x=new_table: self.load_file(x))
    #     self.tables.append(new_table)
    #
    #     curr = len(self.tables)
    #     self.calculate_btn.setEnabled(curr > 1)
    #     self.layout.addWidget(self.tables[-1])
    #     self.layout.addWidget(self.add_btn)
    #     self.layout.addWidget(self.remove_btn)
    #     self.layout.addWidget(self.calculate_btn)
    #     # self.layout.addWidget(self.add_aspect_btn)
    #
    # def remove_table(self, widg):
    #     # Remove the aspect from the display
    #     self.layout.removeWidget(widg)
    #     # self.layout.removeWidget(self.remove_btns[i])
    #     # Remove the aspect from the list
    #     place = self.tables.index(widg)
    #     self.tables.remove(widg)
    #     for k in range(place, len(self.tables)):
    #         # print(self.drop_menu_list[k])
    #         self.layout.addWidget(self.tables[k])
    #     self.layout.addWidget(self.add_btn)
    #     self.layout.addWidget(self.remove_btn)
    #     self.layout.addWidget(self.calculate_btn)
    #     # self.pick_fusion.setEnabled(l > 1)
    #     widg.deleteLater()
    #     # self.check()
    #
    # def load_file(self, btn):
    #     file_name = QFileDialog.getOpenFileName(self, "Open File", "../data", "CSV (*.csv)")
    #     if len(file_name[0]) > 0:
    #         btn.setText(path_leaf(file_name[0]))
    #     elif len(file_name[0]) == 0:
    #         btn.setText("Browse...")

    def set_function(self):
        self.function = self.fusion_func.currentText()

    def set_aspect_1(self):
        self.aspect_1 = self.table_1.currentText()
        if self.aspect_1 is not None and self.aspect_2 is not None:
            self.calc.setEnabled(True)

    def set_aspect_2(self):
        self.aspect_2 = self.table_2.currentText()
        if self.aspect_1 is not None and self.aspect_2 is not None:
            self.calc.setEnabled(True)

    def calculate(self):
        self.controller.create_fusion(self.aspect_1, self.aspect_2, self.function, self.table_widget)
        self.combo_list = self.get_ID()
        self.table_1.clear()
        self.table_1.addItems(self.combo_list)
        self.table_2.clear()
        self.table_2.addItems(self.combo_list)

    def get_ID(self):
        combo_list = []
        aspects_dict = self.controller.system_data.get_aspects()
        for a in list(aspects_dict.keys()):
            combo_list.append("Aspect " + str(a))
        fusions_dict = self.controller.system_data.get_fusions()
        for f in list(fusions_dict.keys()):
            combo_list.append("Fusion " + str(f))
        return combo_list

    def _create_table_editing_widget(self, table_widget):
        """
        :param table_widget: QTable containing content to be displayed.
        :type table_widget: QTableWidget
        :rtype: QWidget
        """

        widget = QWidget()
        widget_layout = QVBoxLayout()
        widget.setLayout(widget_layout)

        # Top widget (Title Label, LoadFromFile Button and SaveAs Button)
        top_widget = QWidget()
        widget_layout.addWidget(top_widget)
        top_layout = QHBoxLayout()
        top_widget.setLayout(top_layout)

        # Bottom widget (QTable)
        if table_widget is None:
            table_widget = QTableWidget(50, 50, self)
            table_widget.resizeColumnsToContents()
        widget_layout.addWidget(table_widget)

        # Contents of top widget
        top_label = QLabel("Fusion table")
        top_layout.addWidget(top_label)
        top_layout.addStretch(1)

        # load_from_file_button = QPushButton("Load From File...")
        # load_from_file_button.setToolTip("Load the  table from a CSV file.") # TODO: eventually add other file types
        # load_from_file_button.clicked.connect(lambda state, qtable = table_widget: self.controller.load_from_csv(self, qtable))
        # top_layout.addWidget(load_from_file_button)

        save_as_csv_button = QPushButton("Save As...")
        save_as_csv_button.setToolTip("Save the fusion table as a CSV file.")  # TODO: eventually add other file types
        save_as_csv_button.clicked.connect(lambda state, qtable = table_widget: self.controller.save_as_csv(self, qtable))
        top_layout.addWidget(save_as_csv_button)

        # if widget_type == "Users":
        #     self.users_table = table_widget
        #     self.layout.addWidget(widget, 0, 0, 1, 3)
        #
        # elif widget_type == "Activities":
        #     self.activities_table = table_widget
        #     self.layout.addWidget(widget, 0, 3, 1, 3)
        #
        # table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        # table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.recommendations_table = table_widget
        # self.layout.addWidget(widget, 1, 0)

        return widget
