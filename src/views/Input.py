from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from .DropMenu import *
from models.Aspect import *


class Input(QWidget):
    def __init__(self, parent=None):
        super(Input, self).__init__(parent)

        self.layout = QGridLayout(self)

        curr_calcul = QLabel("User or Activities!")

        # size_choice = QFormLayout
        #
        # size_choice.addRow("Number of students/activities")
        # size_choice.addRow("Number of properties")

        self.layout.addWidget(curr_calcul, 0, 1)
        # create = QPushButton("Create default table")
        # create.clicked.connect(lambda state, x=5, y=4: self.remove_aspect(x, y))
        # self.layout.addWidget(create, 1, 1)

    # def table(self, r, c):
        # Create a matrix with students on the Y axis, activities on the X axis
        # Get the students from the first line of users' csv files
        # Idem for activities
        users = []  # Student name here
        activities = []  # Activity title here
        aspects = []  # Property here

        c = 4
        r = 5

        self.qtable = QTableWidget(r+1, c+1)
        self.qtable.verticalHeader().setVisible(False)
        self.qtable.horizontalHeader().setVisible(False)
        self.layout.addWidget(self.qtable, 1, 1)

        # Add the actual users and activities to the qtable
        for i in range(1, r+1):
            # item = QTableWidgetItem(users[i-1])
            item = QTableWidgetItem("Student name or Activity title here")
            item.setTextAlignment(Qt.AlignCenter)
            self.qtable.setItem(i, 0, item)

        for i in range(1, c+1):
            # item = QTableWidgetItem(activities[i-1])
            item = QTableWidgetItem("Aspect property here")
            item.setTextAlignment(Qt.AlignCenter)
            self.qtable.setItem(0, i, item)

        # Resize the table to fit its content
        self.qtable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.qtable.resizeColumnsToContents()

        self.layout.addWidget(self.qtable, 2, 2)

        add_row_btn = QPushButton("Add a row")
        add_row_btn.clicked.connect(self.add_row)
        self.layout.addWidget(add_row_btn, 2, 3)

        add_col_btn = QPushButton("Add a column")
        add_col_btn.clicked.connect(self.add_column)
        self.layout.addWidget(add_col_btn, 3, 3)

        remove_row_btn = QPushButton("Remove a row")
        remove_row_btn.clicked.connect(self.remove_row)
        self.layout.addWidget(remove_row_btn, 2, 4)

        remove_col_btn = QPushButton("Remove a column")
        remove_col_btn.clicked.connect(self.remove_column)
        self.layout.addWidget(remove_col_btn, 3, 4)

        self.ok_btn = QPushButton("Save as a .csv")
        # self.ok_btn.clicked.connect(self.save)
        self.layout.addWidget(self.ok_btn, 4, 4)

    def add_row(self):
        self.qtable.insertRow(self.qtable.rowCount())

    def add_column(self):
        self.qtable.insertColumn(self.qtable.columnCount())

    def remove_row(self):
        self.qtable.removeRow(self.qtable.rowCount()-1)

    def remove_column(self):
        self.qtable.removeColumn(self.qtable.columnCount()-1)

    # def save(self):
    #     print("Table saved as a .csv")
    #     # TODO: Actually save it as a .csv!
        # print(type(self.parent()))
        # self.parent.set_page_sorry()

