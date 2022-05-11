import datetime
import os

import PyQt5.QtBluetooth
import pandas as pd
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from calculations import BasicFunctions
import numpy as np

import ntpath

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


class Result(QWidget):

    def __init__(self, system_state, ind, parent=None):
        # Recommendations as seen from the selection side, ie which activity for which student
        super(Result, self).__init__(parent)

        self.system_state = system_state
        # self.layout = QGridLayout(self)

        # Create a matrix with students on the Y axis, activities_names on the X axis

        aspect_name = self.system_state.data.aspects[ind].aspect_type

        users_names = self.system_state.data.aspects[ind].user_names  # for aspect number "ind"
        activities_names = self.system_state.data.aspects[ind].activity_names
        self.func = self.system_state.data.aspects[ind].calc_function

        users = self.system_state.data.aspects[ind].users
        activities = self.system_state.data.aspects[ind].activities

        self.system_state.data.aspects[ind].calculate_recommendations(BasicFunctions.functions[self.func])

        self.rec = self.system_state.data.aspects[ind].chosen_recommendations

        self.users_table = self.create_QTable(users_names, users[:1][0], users)

        self.acts_table = self.create_QTable(activities[:, 0], activities_names, activities)

        self.rec_table = self.create_QTable(users_names, activities_names, self.rec)

        self.table1 = QWidget(self)
        self.table1.layout = QVBoxLayout(self)
        self.table1.layout.addWidget(QLabel("Users Table"))
        self.table1.layout.addWidget(self.users_table)
        # self.change_users_btn = QPushButton("Change Users Table")
        self.browse_users_btn = QRadioButton('Browse')
        # self.table1.layout.addWidget(self.browse_users_btn)
        self.create_users_btn = QRadioButton('Create Table')
        self.bkt_btn = QRadioButton('BKT')
        self.bkt_btn.setToolTip("Create new users table using BKT.")
        radio_widg = QWidget()
        radio_widg.layout = QHBoxLayout(self)
        radio_widg.layout.addWidget(self.browse_users_btn)
        radio_widg.layout.addWidget(self.create_users_btn)
        if aspect_name == "Didactic":  # TODO dynamic check
            radio_widg.layout.addWidget(self.bkt_btn)
        radio_widg.layout.addStretch(1)
        # self.table1.layout.addWidget(self.create_users_btn)

        self.change_users_btn = QPushButton("Modify Table")
        self.change_users_btn.setToolTip("Change the users table.")
        # self.change_users_btn.clicked.connect(self.load_users_file)
        self.change_users_btn.clicked.connect(self.modify_users_table)
        # self.table1.layout.addWidget(self.change_users_btn)
        radio_widg.layout.addWidget(self.change_users_btn)
        # radio_widg.layout.addStretch(1)
        radio_widg.setLayout(radio_widg.layout)
        self.table1.layout.addWidget(radio_widg)
        self.table1.setLayout(self.table1.layout)

        self.table2 = QWidget()
        self.table2.layout = QVBoxLayout(self)
        self.table2.layout.addWidget(QLabel("Activities Table"))
        self.table2.layout.addWidget(self.acts_table)
        self.browse_acts_btn = QRadioButton('Browse')
        # self.table2.layout.addWidget(self.browse_acts_btn)
        self.create_acts_btn = QRadioButton('Create Table')
        # self.table2.layout.addWidget(self.create_acts_btn)

        radio_widg = QWidget()
        radio_widg.layout = QHBoxLayout(self)
        radio_widg.layout.addWidget(self.browse_acts_btn)
        radio_widg.layout.addWidget(self.create_acts_btn)
        radio_widg.layout.addStretch(1)
        self.change_acts_btn = QPushButton("Modify Table")
        self.change_acts_btn.setToolTip("Change the activities table.")
        # self.change_users_btn.clicked.connect(self.load_users_file)
        self.change_acts_btn.clicked.connect(self.modify_acts_table)
        # self.table1.layout.addWidget(self.change_users_btn)
        radio_widg.layout.addWidget(self.change_acts_btn)
        # radio_widg.layout.addStretch(1)
        radio_widg.setLayout(radio_widg.layout)
        self.table2.layout.addWidget(radio_widg)
        # self.change_acts_btn = QPushButton("Modify Table")
        # self.change_acts_btn.setToolTip("Change the activities table.")
        # self.change_acts_btn.clicked.connect(self.load_acts_file)
        # self.change_acts_btn.clicked.connect(self.modify_acts_table)
        # self.table2.layout.addWidget(self.change_acts_btn)
        self.table2.setLayout(self.table2.layout)

        self.table3 = QWidget()
        self.table3.layout = QVBoxLayout(self)
        self.table3.layout.addWidget(QLabel("Recommendation Table"))
        self.table3.layout.addWidget(self.rec_table)
        self.change_func_btn = QComboBox()
        self.change_func_btn.setToolTip("Pick a different calculation function.")
        curr_func = self.func
        self.change_func_btn.setCurrentText(curr_func)
        self.change_func_btn.addItems(BasicFunctions.functions)
        # self.change_func_btn.currentIndexChanged.connect(self.function_picked)
        self.table3.layout.addWidget(self.change_func_btn)
        self.table3.setLayout(self.table3.layout)

        self.table4 = QWidget()
        self.table4.layout = QVBoxLayout(self)
        self.table4.layout.addStretch(5)
        save_csv_btn = QPushButton("Save as .csv")
        self.table4.layout.addWidget(save_csv_btn, Qt.AlignBottom)
        self.table4.layout.addStretch(1)
        save_csv_btn.clicked.connect(self.to_csv)
        recalculate_btn = QPushButton("Recalculate")
        # recalculate_btn.clicked.connect()  # connect to controller's recalculate func
        self.table4.layout.addWidget(recalculate_btn, Qt.AlignBottom)
        self.table4.setLayout(self.table4.layout)
        self.table4.layout.setSpacing(0)

        # self.rec_table = QTableWidget(len(users_names)+1, len(activities_names)+1, self)
        # self.rec_table.verticalHeader().setVisible(False)
        # self.rec_table.horizontalHeader().setVisible(False)
        # self.layout.addWidget(self.rec_table, 1, 0)
        #
        # # Add the actual users_names and activities_names to the rec_table
        # for i in range(1, len(users_names)+1):
        #     item = QTableWidgetItem(users_names[i-1])
        #     item.setTextAlignment(Qt.AlignCenter)
        #     self.rec_table.setItem(i, 0, item)
        #
        # for i in range(1, len(activities_names)+1):
        #     item = QTableWidgetItem(activities_names[i-1])
        #     item.setTextAlignment(Qt.AlignCenter)
        #     self.rec_table.setItem(0, i, item)
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
        #         self.rec_table.setItem(i+1, j+1, item)
        #
        # # for i in range(1, len(activities_names)):
        # #     for j in range(1, len(users_names)):
        # #         print("OK")
        #
        # # Resize the table to fit its content
        # self.rec_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.rec_table.resizeColumnsToContents()
        #
        # # recommandation table cannot be edited
        # self.rec_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.rec_table.setSelectionMode(QAbstractItemView.NoSelection)
        # self.rec_table.setSelectionBehavior(QAbstractItemView.SelectRows)
    # def usersTable or activTable been change:
        # check if the data inside is a number?
        # grey out rec table
        # ungrey recalc button...?

    # def recalculate(self):
        # if the qtables have been modified => import to_csv or to_df or smth with input.py's function
        # recalc
        # update the rec table with the new results

    def to_csv(self):
        col_count = self.rec_table.columnCount()
        row_count = self.rec_table.rowCount()
        headers = [str(self.rec_table.item(0, i).text()) for i in range(1, col_count)]
        ind = [str(self.rec_table.item(i, 0).text()) for i in range(1, row_count)]
        df_row = []
        for row in range(1, row_count):
            df_col = []
            for col in range(1, col_count):
                table_item = self.rec_table.item(row, col)
                df_col.append('' if table_item is None else str(table_item.text()))
            df_row.append(df_col)

        df = pd.DataFrame(df_row, index=ind, columns=headers)
        self.save_as_csv(df)

    def save_as_csv(self, df):
        default_dir = "../data"
        default_filename = os.path.join(default_dir, "recommendations")
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save CSV file", default_filename, "CSV Files (*.csv)"
        )
        if len(filename) > 0:
            name = filename
            df.to_csv(name)
            print(name)
            print(filename)

    def modify_users_table(self):
        if self.browse_users_btn.isChecked():
            self.load_users_file()

    def modify_acts_table(self):
        if self.browse_acts_btn.isChecked():
            self.load_acts_file()

    def load_users_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", "../data", "CSV (*.csv)")
        if len(file_name[0]) > 0:
            self.change_users_btn.setText(path_leaf(file_name[0]))
            self.change_users_table(file_name[0])
        elif len(file_name[0]) == 0:
            self.change_users_btn.setText("Browse...")

    def load_acts_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", "../data", "CSV (*.csv)")
        if len(file_name[0]) > 0:
            self.change_acts_btn.setText(path_leaf(file_name[0]))
        elif len(file_name[0]) == 0:
            self.change_acts_btn.setText("Browse...")

    def change_users_table(self, users_file):
        users_df = pd.read_csv(users_file, sep=',', index_col=0)
        users = np.array(users_df)
        users = users.T
        user_names = list(users_df.columns.values)
        self.users_table = self.create_QTable(user_names, users[:1][0], users)
        # self.table1.users_table = self.users_table

    def create_QTable(self, y, x, body):
        y_size = len(y) + 1
        x_size = len(x) + 1
        qtable = QTableWidget(y_size, x_size, self)
        qtable.verticalHeader().setVisible(False)
        qtable.horizontalHeader().setVisible(False)

        for i in range(1, y_size):
            item = QTableWidgetItem(y[i - 1])
            item.setTextAlignment(Qt.AlignCenter)
            qtable.setItem(i, 0, item)

        for i in range(1, x_size):
            item = QTableWidgetItem(x[i - 1])
            item.setTextAlignment(Qt.AlignCenter)
            qtable.setItem(0, i, item)

        for i in range(y_size - 1):
            for j in range(x_size - 1):
                s = str(body[i][j])
                item = QTableWidgetItem(s)
                item.setTextAlignment(Qt.AlignCenter)
                qtable.setItem(i + 1, j + 1, item)

        # Resize the table to fit its content
        qtable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        qtable.resizeColumnsToContents()

        # recommandation table cannot be edited
        qtable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        qtable.setSelectionMode(QAbstractItemView.NoSelection)
        qtable.setSelectionBehavior(QAbstractItemView.SelectRows)

        return qtable

# class TableUser(QWidget):
#
#     def __init__(self, parent=None):
#         super(TableUser, self).__init__(parent)
#         self.layout = QVBoxLayout(self)
#         self.users_table = QTableWidget(self)
#         self.layout.addWidget(self.users_table)
#         # self.change_users_btn = QPushButton("Change Users Table")
#         self.change_users_btn = QPushButton("Browse...")
#         self.change_users_btn.setToolTip("Change the users table.")
#         self.change_users_btn.clicked.connect(Result.load_users_file)
#         self.layout.addWidget(self.change_users_btn)
#         self.setLayout(self.layout)
