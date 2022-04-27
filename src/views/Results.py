import PyQt5.QtBluetooth
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from calculations import BasicFunctions


class Results(QWidget):

    def __init__(self, system_state, parent=None):
        # Recommendations as seen from the selection side, ie which activity for which student
        super(Results, self).__init__(parent)

        self.system_state = system_state
        self.layout = QGridLayout(self)

        # Create a matrix with students on the Y axis, activities on the X axis
        # Get the students from the first line of users' csv files
        # Idem for activities
        users = self.system_state.data.aspects[0].user_names  # exemple, to test the code, for one aspect only
        activities = self.system_state.data.aspects[0].activity_names
        # print("hello")
        func = self.system_state.data.aspects[0].calc_function

        if func == BasicFunctions.functions[0]:
            self.system_state.data.aspects[0].calculate_recommendations(BasicFunctions.product)
        elif func == BasicFunctions.functions[1]:
            self.system_state.data.aspects[0].calculate_recommendations(BasicFunctions.distance)
        elif func == BasicFunctions.functions[2]:
            self.system_state.data.aspects[0].calculate_recommendations(BasicFunctions.time)

        rec = self.system_state.data.aspects[0].recommendations

        curr_calcul = QLabel(f"Function {func} has been applied.")
        self.layout.addWidget(curr_calcul, 0, 1)

        self.qtable = QTableWidget(len(users)+1, len(activities)+1, self)
        # self.qtable = QTableWidget(3, 4)
        self.qtable.verticalHeader().setVisible(False)
        self.qtable.horizontalHeader().setVisible(False)
        self.layout.addWidget(self.qtable, 1, 1)

        # Add the actual users and activities to the qtable
        for i in range(1, len(users)+1):
            item = QTableWidgetItem(users[i-1])
            item.setTextAlignment(Qt.AlignCenter)
            self.qtable.setItem(i, 0, item)

        for i in range(1, len(activities)+1):
            item = QTableWidgetItem(activities[i-1])
            item.setTextAlignment(Qt.AlignCenter)
            self.qtable.setItem(0, i, item)

        # for now let it be empty
        # display the rec table
        for i in range(len(users)):
            for j in range(len(activities)):
                # print(r[i][j])
                s = str(rec[i][j])
                item = QTableWidgetItem(s)
                # item.setData(Qt.DisplayRole, r[i][j])
                item.setTextAlignment(Qt.AlignCenter)
                self.qtable.setItem(i+1, j+1, item)

        # for i in range(1, len(activities)):
        #     for j in range(1, len(users)):
        #         print("OK")

        # Resize the table to fit its content
        self.qtable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.qtable.resizeColumnsToContents()

        # recommandation table cannot be edited
        self.qtable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.qtable.setSelectionMode(QAbstractItemView.NoSelection)
        self.qtable.setSelectionBehavior(QAbstractItemView.SelectRows)
