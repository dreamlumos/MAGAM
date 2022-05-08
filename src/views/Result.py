import PyQt5.QtBluetooth
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from calculations import BasicFunctions
import numpy as np


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
        func = self.system_state.data.aspects[ind].calc_function

        users = self.system_state.data.aspects[ind].users
        activities = self.system_state.data.aspects[ind].activities

        # Check the function picked by the user against the list of functions in BasicFunctions and calculate accordingly
        if func == BasicFunctions.functions[0]:
            self.system_state.data.aspects[ind].calculate_recommendations(BasicFunctions.product)
        elif func == BasicFunctions.functions[1]:
            self.system_state.data.aspects[ind].calculate_recommendations(BasicFunctions.distance)
        elif func == BasicFunctions.functions[2]:
            self.system_state.data.aspects[ind].calculate_recommendations(BasicFunctions.time)

        self.rec = self.system_state.data.aspects[ind].recommendations

        # curr_calcul = QLabel(f"Function {func} has been applied.")
        # self.layout.addWidget(curr_calcul, 0, 1)  # TODO modify the layout to fit better what we want to be able to do once we've calculated
        # users_rec = users[1:, 1:]
        self.users_table = self.create_QTable(users_names, users[:1][0], users)
        # self.layout.addWidget(self.users_table, 0, 0)

        # acts_rec = activities[1:, 1:]
        self.acts_table = self.create_QTable(activities[:, 0], activities_names, activities)
        # self.layout.addWidget(self.acts_table, 0, 1)

        self.qtable_rec = self.create_QTable(users_names, activities_names, self.rec)
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

        for i in range(y_size-1):
            for j in range(x_size-1):
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
