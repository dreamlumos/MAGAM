import PyQt5.QtBluetooth
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .Result import *
from .FusionTab import *
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
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(lambda index: self.tabs.removeTab(index))
        # TODO add csv button
        # TODO add recalculate button
    # def getResult(self):
        for i in range(self.asp_size):
            self.create_tab(i)
            # for i in range(len(title_list)):
            # self.add_tabs(Result(self.system_state, i, self), system_state.data.aspects[i].aspect_type)
            # self.add_tabs(QWidget(), title_list[i])
        self.add_tabs(FusionTab(self.system_state, self), "Fusion")  # Fusion
        self.tab_button = QToolButton(self)
        self.tab_button.setText(' + ')
        # font = self.tab_button.font()
        # font.setBold(True)
        # self.tab_button.setFont(font)
        self.tabs.setCornerWidget(self.tab_button)
        self.tab_button.setToolTip("Open a new tab")
        self.tab_button.clicked.connect(self.add_page)

    def add_page(self):
        self.tabs.addTab(QWidget(), "New Tab")

    def add_tabs(self, tab, title):
        self.tabs.addTab(tab, title)
        # self.tabs.insertTab(tab, "")

    def create_tab(self, indice):
        layout = QVBoxLayout()

        splitter = QSplitter(Qt.Horizontal)

        tab = QWidget()
        tab.layout = QGridLayout(self)
        title = self.system_state.data.aspects[indice].aspect_type
        rec = Result(self.system_state, indice, self)

        # table1 = QWidget()
        # table1.layout = QVBoxLayout(self)
        # table1.layout.addWidget(rec.users_table)
        # table1.layout.addWidget(QPushButton("Change Users Table"))
        # table1.setLayout(table1.layout)
        tab.layout.addWidget(rec.table1, 0, 0, 1, 2)

        # table2 = QWidget()
        # table2.layout = QVBoxLayout(self)
        # table2.layout.addWidget(rec.acts_table)
        # table2.layout.addWidget(QPushButton("Change Activities Table"))
        # table2.setLayout(table2.layout)
        tab.layout.addWidget(rec.table2, 0, 2, 1, 2)

        # table3 = QWidget()
        # table3.layout = QVBoxLayout(self)
        # table3.layout.addWidget(rec.qtable_rec)
        # table3.layout.addWidget(QPushButton("function"))
        # table3.setLayout(table3.layout)
        tab.layout.addWidget(rec.table3, 1, 0, 1, 3)  # if i add the buttons directly to Results/createQTable, how do i link them?

        # table4 = QWidget()
        # table4.layout = QVBoxLayout(self)
        # table4.layout.addWidget(QPushButton("Save as .csv"))
        # table4.layout.addWidget(QPushButton("Recalculate"))
        # table4.setLayout(table4.layout)
        # table4.layout.setSpacing(0)
        tab.layout.addWidget(rec.table4, 1, 3, 1, 1)

        tab.setLayout(tab.layout)
        splitter.addWidget(tab)
        splitter.addWidget(QTextEdit())

        self.add_tabs(tab, title)

    # @pyqtSlot()
    # def on_click(self):
    #     print("\n")
    #     for currentQTableWidgetItem in self.tableWidget.selectedItems():
    #         print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
