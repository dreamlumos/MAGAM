import datetime
import ntpath
import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from calculations import *
from models.Aspect import *


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


class AspectTab(QWidget):

    def __init__(self, controller, aspect_id, aspect_type=None, users_qtable=None, activities_qtable=None, recommendations_qtable=None, function=None, parent=None):
        super().__init__(parent)

        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        self.controller = controller
        self.parent = parent
        self.aspect_id = aspect_id

        self.aspect_type = aspect_type
        self.function = function

        self.users_widget = self._create_table_editing_widget("Users", users_qtable)
        self.activities_widget = self._create_table_editing_widget("Activities", activities_qtable)
        self.recommendations_widget = self._create_table_editing_widget("Recommendations", recommendations_qtable)
        if users_qtable is None:
            recalc = False
        else: 
            recalc = True
        self.buttons_widget = self._create_buttons_widget(aspect_type, function, recalc)

    # def create_QTable(self, y, x, body):
    #     y_size = len(y) + 1
    #     x_size = len(x) + 1
    #     qtable = QTableWidget(y_size, x_size, self)
    #     qtable.verticalHeader().setVisible(False)
    #     qtable.horizontalHeader().setVisible(False)

    #     for i in range(1, y_size):
    #         item = QTableWidgetItem(y[i - 1])
    #         item.setTextAlignment(Qt.AlignCenter)
    #         qtable.setItem(i, 0, item)

    #     for i in range(1, x_size):
    #         item = QTableWidgetItem(x[i - 1])
    #         item.setTextAlignment(Qt.AlignCenter)
    #         qtable.setItem(0, i, item)

    #     for i in range(y_size - 1):
    #         for j in range(x_size - 1):
    #             s = str(body[i][j])
    #             item = QTableWidgetItem(s)
    #             item.setTextAlignment(Qt.AlignCenter)
    #             qtable.setItem(i + 1, j + 1, item)

    #     # Resize the table to fit its content
    #     qtable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
    #     qtable.resizeColumnsToContents()

    #     # recommandation table cannot be edited
    #     qtable.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #     qtable.setSelectionMode(QAbstractItemView.NoSelection)
    #     qtable.setSelectionBehavior(QAbstractItemView.SelectRows)

    #     return qtable

    def set_index(self, tab_index):
        self.tab_index = tab_index

    def set_aspect_type(self):
        self.aspect_type = self.change_aspect_type_menu.currentText()
        self.parent.tabs.setTabText(self.tab_index, self.aspect_type)
        self.check_filled()

    def set_function(self):
        self.function = self.change_function_menu.currentText()
        self.check_filled()

    def _create_table_editing_widget(self, widget_type, table_widget):
        """
        :param widget_type: type of widget. One of "Users", "Activities", "Recommendations".
        :param table_widget: QTable containing content to be displayed.
        :type widget_type: str
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
        top_label = QLabel(widget_type)
        top_layout.addWidget(top_label)
        top_layout.addStretch(1)

        load_from_file_button = QPushButton("Load From File...")
        load_from_file_button.setToolTip("Load the "+widget_type+" table from a CSV file.") # TODO: eventually add other file types
        load_from_file_button.clicked.connect(lambda state, qtable = table_widget: self.controller.load_from_csv(self, qtable))
        top_layout.addWidget(load_from_file_button)

        save_as_csv_button = QPushButton("Save As...")
        save_as_csv_button.setToolTip("Save the "+widget_type+" table as a CSV file.") # TODO: eventually add other file types
        save_as_csv_button.clicked.connect(lambda state, qtable = table_widget: self.controller.save_as_csv(self, qtable))
        top_layout.addWidget(save_as_csv_button)

        if widget_type == "Users":
            self.users_table = table_widget
            self.layout.addWidget(widget, 0, 0, 1, 3)

        elif widget_type == "Activities":
            self.activities_table = table_widget
            self.layout.addWidget(widget, 0, 3, 1, 3)

        elif widget_type == "Recommendations":
            table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            table_widget.setSelectionMode(QAbstractItemView.NoSelection)
            table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.recommendations_table = table_widget
            self.layout.addWidget(widget, 1, 0, 1, 5)

        return widget

    def _create_buttons_widget(self, aspect_type=None, function=None, recalc=False):

        widget = QWidget()
        widget_layout = QGridLayout()
        widget.setLayout(widget_layout)

        clear_button = QPushButton("Clear all tables")
        clear_button.clicked.connect(self.reset_all_widgets)

        self.change_aspect_type_menu = QComboBox()
        self.change_aspect_type_menu.addItems(Aspect.aspect_types)
        self.change_aspect_type_menu.setPlaceholderText("------")
        # if aspect_type is not None:
        if type(aspect_type) == str:
            self.change_aspect_type_menu.setCurrentText(aspect_type)
        # else:
        #     self.calculate_button.enabled(False)
        self.change_aspect_type_menu.currentIndexChanged.connect(self.set_aspect_type)

        self.change_function_menu = QComboBox()
        self.change_function_menu.setToolTip("Pick a different calculation function.")
        self.change_function_menu.setPlaceholderText("------")  # placeholder not showing is a bug on Qt's side

        self.change_function_menu.addItems(basic_functions)

        if recalc:
            self.calculate_button = QPushButton("Recalculate")
        else:
            self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)
        self.calculate_button.setEnabled(False)

        # if function is not None:
        if type(function) == str:
            self.change_function_menu.setCurrentText(function)

        self.change_function_menu.currentIndexChanged.connect(self.set_function)

        widget_layout.addWidget(clear_button, 0, 0, 1, 1)
        widget_layout.setRowStretch(1, 1)
        widget_layout.addWidget(QLabel("Aspect type"), 2, 0, 1, 1)
        widget_layout.addWidget(self.change_aspect_type_menu, 3, 0, 1, 1)
        widget_layout.setRowStretch(4, 1)
        widget_layout.addWidget(QLabel("Function to apply"), 5, 0, 1, 1)
        widget_layout.addWidget(self.change_function_menu, 6, 0, 1, 1)
        widget_layout.addWidget(self.calculate_button, 7, 0, 1, 1)

        self.layout.addWidget(widget, 1, 5, 1, 1)

        return widget

    def reset_recommendations(self):
        self.recommendations_table.clear()
        self.calculate_button.setText("Recalculate")

    def reset_all_widgets(self):
        self.users_table.clear()
        self.activities_table.clear()
        self.recommendations_table.clear()
        self.calculate_button.setText("Calculate")
        # self.calculate_button.enabled(False)

    def calculate(self):
        self.controller.update_aspect_from_qtables(self.aspect_id, self.aspect_type, self.users_table, self.activities_table, self.recommendations_table, self.function)

    def check_filled(self):
        if self.aspect_type is None:
            self.filled = False
        # elif self.users_table is None:
        #     self.filled = False
        # elif self.activities_table is None:
        #     self.filled = False
        elif self.function is None:
            self.filled = False
        else:
            self.filled = True

        if self.filled == False:
            self.calculate_button.setEnabled(False)
        else:
            self.calculate_button.setEnabled(True)

