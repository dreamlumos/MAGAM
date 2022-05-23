import datetime
import ntpath
import os

import PyQt5.QtBluetooth
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from fusion import *
import utils


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


class FusionTab(QWidget):

    def __init__(self, controller, recommendations_qtable=None, function=None, parent=None):
        super().__init__(parent)

        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        self.controller = controller
        self.controller.set_fusion_tab(self)
        self.parent = parent

        self.function = function
        self.aspect_1 = None
        self.aspect_2 = None

        self.combobox_list = []

        top_widget = QWidget()
        t_layout = QHBoxLayout()
        self.table_1 = QComboBox()
        # self.table_1.setPlaceholderText("NO")
        self.aspect_1 = self.table_1.currentText()
        self.table_1.addItems(self.combobox_list)
        self.table_1.currentIndexChanged.connect(self.set_aspect_1)
        t_layout.addWidget(self.table_1)

        self.fusion_func = QComboBox()
        self.fusion_func.addItems(fusion_functions)
        self.function = self.fusion_func.currentText()
        self.fusion_func.currentIndexChanged.connect(self.set_function)
        t_layout.addWidget(self.fusion_func)

        self.table_2 = QComboBox()
        # self.table_2.setPlaceholderText("NO")
        self.aspect_2 = self.table_2.currentText()
        self.table_2.addItems(self.combobox_list)
        self.table_2.currentIndexChanged.connect(self.set_aspect_2)
        t_layout.addWidget(self.table_2)

        self.controller.update_fusion_tab()

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
        save_as_csv_button.clicked.connect(lambda state, qtable=self.table_widget: utils.save_as_csv(self, qtable))
        b_layout.addWidget(save_as_csv_button)

        self.layout.addWidget(bottom_widget, 1, 0)

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

        self.table_1.clear()
        self.table_1.addItems(self.combobox_list)
        self.table_2.clear()
        self.table_2.addItems(self.combobox_list)

    def update_combobox_list(self, combobox_list):
        self.combobox_list = combobox_list
        self.table_1.clear()
        self.table_1.addItems(self.combobox_list)
        self.table_2.clear()
        self.table_2.addItems(self.combobox_list)

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

        save_as_csv_button = QPushButton("Save As...")
        save_as_csv_button.setToolTip("Save the fusion table as a CSV file.")  # TODO: eventually add other file types
        save_as_csv_button.clicked.connect(lambda state, qtable = table_widget: utils.save_as_csv(self, qtable))
        top_layout.addWidget(save_as_csv_button)

        return widget
