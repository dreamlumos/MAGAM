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
        if users_qtable == None:
            recalc = False
        else: 
            recalc = True
        self.buttons_widget = self._create_buttons_widget(aspect_type, function, recalc)




        # self.table4 = QWidget()
        # self.matrix_toggle = QRadioButton()
        # self.list_toggle = QRadioButton()
        # self.matrix_toggle.setText("Table View")
        # self.list_toggle.setText("List View")
        # self.table4.layout = QVBoxLayout(self)
        # self.table4.layout.addStretch(5)
        # self.table4.layout.addWidget(self.matrix_toggle)
        # self.table4.layout.addStretch(1)
        # self.table4.layout.addWidget(self.list_toggle)
        # self.table4.layout.addStretch(3)
        # self.change_func_btn = QComboBox()
        # self.change_func_btn.setToolTip("Pick a different calculation function.")
        # # curr_func = self.func
        # self.change_func_btn.setCurrentText("------")
        # self.change_func_btn.addItems(BasicFunctions.basic_functions)
        # # self.change_func_btn.currentIndexChanged.connect(self.function_picked)
        # self.table4.layout.addWidget(self.change_func_btn)
        # self.table4.layout.addStretch(1)
        # save_csv_btn.clicked.connect(self.to_csv)
        # recalculate_btn = QPushButton("Recalculate")
        # # recalculate_btn.clicked.connect()
        # self.table4.layout.addWidget(recalculate_btn, Qt.AlignBottom)
        # self.table4.layout.addStretch(1)
        # self.table4.setLayout(self.table4.layout)
        # self.table4.layout.setSpacing(0)

        # self.qtable_rec = QTableWidget(len(users_names)+1, len(activities_names)+1, self)
        # self.qtable_rec.verticalHeader().setVisible(False)
        # self.qtable_rec.horizontalHeader().setVisible(False)
        # self.layout.addWidget(self.qtable_rec, 1, 0)
        #
        # # Add the actual users_names and activities_names to the qtable_rec
        # for i in range(1, len(users_names)+1):
        #     item = QTableWidgetItem(users_names[i-1])
        #     item.setTextAlignment(Qt.AlignCenter)
        #     self.qtable_rec.setItem(i, 0, item)
        #
        # for i in range(1, len(activities_names)+1):
        #     item = QTableWidgetItem(activities_names[i-1])
        #     item.setTextAlignment(Qt.AlignCenter)
        #     self.qtable_rec.setItem(0, i, item)
        #
        # # for now let it be empty
        # # display the rec table
        # for i in range(len(users_names)):
        #     for j in range(len(activities_names)):
        #         # print(r[i][j])
        #         s = str(rec[i][j])
        #         item = QTableWidgetItem(s)
        #         # item.setData(Qt.DisplayRole, r[i][j])
        #         item.setTextAlignment(Qt.AlignCenter)
        #         self.qtable_rec.setItem(i+1, j+1, item)
        #
        # # for i in range(1, len(activities_names)):
        # #     for j in range(1, len(users_names)):
        # #         print("OK")
        #
        # # Resize the table to fit its content
        # self.qtable_rec.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.qtable_rec.resizeColumnsToContents()
        #
        # # recommandation table cannot be edited
        # self.qtable_rec.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.qtable_rec.setSelectionMode(QAbstractItemView.NoSelection)
        # self.qtable_rec.setSelectionBehavior(QAbstractItemView.SelectRows


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

    def set_function(self):
        self.function = self.change_function_menu.currentText()

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
        if table_widget == None:
            table_widget = QTableWidget(50, 50, self)
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
        self.change_aspect_type_menu.setPlaceholderText("------")
        if aspect_type != None:
            self.change_aspect_type_menu.setCurrentText(aspect_type) # TODO: not working rn
        self.change_aspect_type_menu.addItems(Aspect.aspect_types)
        self.change_aspect_type_menu.currentIndexChanged.connect(self.set_aspect_type)

        self.change_function_menu = QComboBox()
        self.change_function_menu.setToolTip("Pick a different calculation function.")
        self.change_function_menu.setPlaceholderText("------")
        if function != None:
            self.change_function_menu.setCurrentText(function) # TODO: not working rn
        self.change_function_menu.addItems(basic_functions)
        self.change_function_menu.currentIndexChanged.connect(self.set_function)

        if recalc:
            self.calculate_button = QPushButton("Recalculate")
        else:
            self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)

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

    def calculate(self):
        self.controller.update_aspect_from_qtables(self.aspect_id, self.aspect_type, self.users_table, self.activities_table, self.recommendations_table, self.function)
