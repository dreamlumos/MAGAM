from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Results(QWidget):

    def __init__(self, parent=None):
        # Results as seen from the selection side, ie which activity for which student
        super(Results, self).__init__(parent)

        self.layout = QGridLayout(self)

        curr_calcul = QLabel("Current calcul is [1] applied on [2] !")
        self.layout.addWidget(curr_calcul, 0, 1)

        # Create a matrix with students on the Y axis, activities on the X axis
        # Get the students from the first line of users' csv files
        # Idem for activities
        users = ['A', 'B', 'C', 'D']  # exemple, to test the code
        activities = ['a1', 'a2', 'a3']

        self.qtable = QTableWidget(len(users)+1, len(activities)+1, self)
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

        # Resize the table to fit its content
        self.qtable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.qtable.resizeColumnsToContents()

        # recommandation table cannot be edited
        self.qtable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.qtable.setSelectionMode(QAbstractItemView.NoSelection)
        self.qtable.setSelectionBehavior(QAbstractItemView.SelectRows)
