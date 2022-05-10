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
        # Get the students from the first line of users_names' csv files
        # Idem for activities_names
        users_names = self.system_state.data.aspects[ind].user_names  # for aspect number "ind"
        activities_names = self.system_state.data.aspects[ind].activity_names
        self.func = self.system_state.data.aspects[ind].calc_function

        users = self.system_state.data.aspects[ind].users
        activities = self.system_state.data.aspects[ind].activities

        # Check the function picked by the user against the list of functions in BasicFunctions and calculate accordingly
        if self.func == BasicFunctions.functions[0]:
            self.system_state.data.aspects[ind].calculate_recommendations(BasicFunctions.product)
        elif self.func == BasicFunctions.functions[1]:
            self.system_state.data.aspects[ind].calculate_recommendations(BasicFunctions.distance)
        elif self.func == BasicFunctions.functions[2]:
            self.system_state.data.aspects[ind].calculate_recommendations(BasicFunctions.time)

        self.rec = self.system_state.data.aspects[ind].chosen_recommendations

        # curr_calcul = QLabel(f"Function {func} has been applied.")
        # self.layout.addWidget(curr_calcul, 0, 1)
        # users_rec = users[1:, 1:]

        self.users_table = self.create_QTable(users_names, users[:1][0], users)
        # self.layout.addWidget(self.users_table, 0, 0)

        # acts_rec = activities[1:, 1:]
        self.acts_table = self.create_QTable(activities[:, 0], activities_names, activities)
        # self.layout.addWidget(self.acts_table, 0, 1)

        self.qtable_rec = self.create_QTable(users_names, activities_names, self.rec)
        # self.table1 = self.create_table1()
        # self.table2 = self.create_table2()
        # self.table4 = self.create_table4()

        # self.table1 = TableUser(self)
        # self.table1.users_table = self.users_table

        self.table1 = QWidget()
        self.table1.layout = QVBoxLayout(self)
        self.table1.layout.addWidget(self.users_table)
        # self.change_users_btn = QPushButton("Change Users Table")
        self.change_users_btn = QPushButton("Browse...")
        self.change_users_btn.setToolTip("Change the users table.")
        self.change_users_btn.clicked.connect(self.load_users_file)
        self.table1.layout.addWidget(self.change_users_btn)
        self.table1.setLayout(self.table1.layout)

        self.table2 = QWidget()
        self.table2.layout = QVBoxLayout(self)
        self.table2.layout.addWidget(self.acts_table)
        self.change_acts_btn = QPushButton("Browse")
        self.change_acts_btn.setToolTip("Change the activities table.")
        self.change_acts_btn.clicked.connect(self.load_acts_file)
        self.table2.layout.addWidget(self.change_acts_btn)
        self.table2.setLayout(self.table2.layout)

        self.table3 = QWidget()
        self.table3.layout = QVBoxLayout(self)
        self.table3.layout.addWidget(self.qtable_rec)
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
        save_csv_btn = QPushButton("Save as .csv")
        self.table4.layout.addWidget(save_csv_btn)
        save_csv_btn.clicked.connect(self.to_csv)
        recalculate_btn = QPushButton("Recalculate")
        # recalculate_btn.clicked.connect()
        self.table4.layout.addWidget(recalculate_btn)
        self.table4.setLayout(self.table4.layout)
        self.table4.layout.setSpacing(0)

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
        # self.qtable_rec.setSelectionBehavior(QAbstractItemView.SelectRows)

    def to_csv(self):
        col_count = self.qtable_rec.columnCount()
        row_count = self.qtable_rec.rowCount()
        headers = [str(self.qtable_rec.item(0, i).text()) for i in range(1, col_count)]
        ind = [str(self.qtable_rec.item(i, 0).text()) for i in range(1, row_count)]
        df_row = []
        for row in range(1, row_count):
            df_col = []
            for col in range(1, col_count):
                table_item = self.qtable_rec.item(row, col)
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


    # def create_table1(self):
    #     table1 = QWidget()
    #     table1.layout = QVBoxLayout(self)
    #     table1.layout.addWidget(self.users_table)
    #     self.change_users_btn = QPushButton("Change Users Table")
    #     table1.layout.addWidget(self.change_users_btn)
    #     table1.setLayout(table1.layout)
    #     # tab.layout.addWidget(table1, 0, 0)
    #     return table1

    # def create_table2(self):
    #     table1 = QWidget()
    #     table1.layout = QVBoxLayout(self)
    #     table1.layout.addWidget(self.acts_table)
    #     self.change_acts_btn = QPushButton("Change Activities Table")
    #     table1.layout.addWidget(self.change_acts_btn)
    #     table1.setLayout(table1.layout)
    #     # tab.layout.addWidget(table1, 0, 0)
    #     return table1

    # def function_picked(self):
    #     self.aspect_type = self.cb_aspect.currentText()

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
