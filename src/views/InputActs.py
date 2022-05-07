import datetime

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from .DropMenu import *
from models.Aspect import *
import pandas
import time


class InputActs(QWidget):
    def __init__(self, parent=None):
        super(InputActs, self).__init__(parent)

        self.layout = QGridLayout(self)

        self.file_name = None

        curr_calcul = QLabel("Activities")

        self.layout.addWidget(curr_calcul, 0, 1)
        # create = QPushButton("Create default table")
        # create.clicked.connect(lambda state, x=5, y=4: self.remove_aspect(x, y))
        # self.layout.addWidget(create, 1, 1)

        c = 3
        r = 4

        self.qtable = QTableWidget(r+1, c+1)
        self.qtable.verticalHeader().setVisible(False)
        self.qtable.horizontalHeader().setVisible(False)
        self.layout.addWidget(self.qtable, 1, 1)

        # Add the actual users and activities to the qtable
        for i in range(1, r+1):
            # item = QTableWidgetItem(users[i-1])
            item = QTableWidgetItem("Activity title here")
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
        self.ok_btn.clicked.connect(self.save_as_csv)
        self.layout.addWidget(self.ok_btn, 4, 4)

        self.cancel_btn = QPushButton("Cancel")
        self.layout.addWidget(self.cancel_btn, 4, 3)

    def add_row(self):
        self.qtable.insertRow(self.qtable.rowCount())

    def add_column(self):
        self.qtable.insertColumn(self.qtable.columnCount())

    def remove_row(self):
        self.qtable.removeRow(self.qtable.rowCount()-1)

    def remove_column(self):
        self.qtable.removeColumn(self.qtable.columnCount()-1)

    def save_as_csv(self):
        col_count = self.qtable.columnCount()
        row_count = self.qtable.rowCount()
        headers = [str(self.qtable.item(0, i).text()) for i in range(1,col_count)]
        ind = [str(self.qtable.item(i, 0).text()) for i in range(1,row_count)]
        print(headers)
        print(ind)

        df_row = []
        for row in range(1,row_count):
            df_col = []
            for col in range(1,col_count):
                table_item = self.qtable.item(row, col)
                df_col.append('' if table_item is None else str(table_item.text()))
            df_row.append(df_col)

        df = pandas.DataFrame(df_row, index=ind, columns=headers)
        name = 'activities_input_' + str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.csv'
        df.to_csv(name)
        print(name)
        self.file_name = name

    # def back(self):
    #


