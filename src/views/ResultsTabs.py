import PyQt5.QtBluetooth
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .Result import *
from PyQt5.QtCore import *


# from calculations import BasicFunctions


class ResultsTabs(QWidget):

    def __init__(self, system_state, parent=None):
        # Recommendations as seen from the selection side, ie which activity for which student
        super(ResultsTabs, self).__init__(parent)

        self.system_state = system_state
        self.asp_size = len(self.system_state.data.aspects)
        self.layout = QHBoxLayout(self)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        # TODO add csv button
        # TODO add recalculate button
    # def getResult(self):
        for i in range(self.asp_size):
            self.create_tab(i)
            # for i in range(len(title_list)):
            # self.add_tabs(Result(self.system_state, i, self), system_state.data.aspects[i].aspect_type)
            # self.add_tabs(QWidget(), title_list[i])
        # self.add_tabs()  # Fusion

    def add_tabs(self, tab, title):
        self.tabs.addTab(tab, title)
        # self.tabs.insertTab(tab, "")

    def create_tab(self, indice):
        tab = QWidget()
        tab.layout = QGridLayout(self)
        title = self.system_state.data.aspects[indice].aspect_type
        rec = Result(self.system_state, indice, self)

        table1 = QWidget()
        table1.layout = QVBoxLayout(self)
        table1.layout.addWidget(rec.users_table)
        table1.layout.addWidget(QPushButton("Change Users Table"))
        table1.setLayout(table1.layout)
        tab.layout.addWidget(table1, 0, 0)

        table2 = QWidget()
        table2.layout = QVBoxLayout(self)
        table2.layout.addWidget(rec.acts_table)
        table2.layout.addWidget(QPushButton("Change Activities Table"))
        table2.setLayout(table2.layout)
        tab.layout.addWidget(table2, 0, 1)

        table3 = QWidget()
        table3.layout = QVBoxLayout(self)
        table3.layout.addWidget(rec.qtable_rec)
        table3.layout.addWidget(QPushButton("Recalculate"))
        table3.setLayout(table3.layout)
        tab.layout.addWidget(table3, 1, 0)  # if i add the buttons directly to Results/createQTable, how do i link them?

        tab.setLayout(tab.layout)
        self.add_tabs(tab, title)

    # @pyqtSlot()
    # def on_click(self):
    #     print("\n")
    #     for currentQTableWidgetItem in self.tableWidget.selectedItems():
    #         print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
