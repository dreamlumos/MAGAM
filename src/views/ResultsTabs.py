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
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        # TODO add csv button
        # TODO add recalculate button
    # def getResult(self):
        for i in range(self.asp_size):
            # for i in range(len(title_list)):
            self.add_tabs(Result(self.system_state, i, self), system_state.data.aspects[i].aspect_type)  # TODO modified here
            # self.add_tabs(QWidget(), title_list[i])
        # self.add_tabs()  # Fusion

    def add_tabs(self, tab, title):
        self.tabs.addTab(tab, title)
        # self.tabs.insertTab(tab, "")

    # @pyqtSlot()
    # def on_click(self):
    #     print("\n")
    #     for currentQTableWidgetItem in self.tableWidget.selectedItems():
    #         print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
