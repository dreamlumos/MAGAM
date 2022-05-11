import PyQt5.QtBluetooth
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .Aspects import *
from .Result import *
from .EmptyTab import *
from .FusionTab import *
from models.Aspect import *
from PyQt5.QtCore import *


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
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(lambda index: self.tabs.removeTab(index))

        # self.main_menu = QWidget()
        # self.main_menu.layout = QHBoxLayout(self)
        # qtable = QTableWidget(1000, 1000, self)
        # self.main_menu.layout.addWidget(qtable)
        # self.main_menu.setLayout(self.main_menu.layout)
        # self.tabs.addTab(self.main_menu, "Main Menu")

        self.tabs.addTab(Aspects(system_state, self), "Aspects")
        self.tabs.tabBar().setTabButton(0, QTabBar.RightSide, None)

        # TODO add csv button
        # TODO add recalculate button

        for i in range(self.asp_size):
            self.create_tab(i)

        self.add_tabs(FusionTab(self.system_state, self), "Fusion")  # Fusion
        self.tab_button = QPushButton(self)
        self.tab_button.setText(' + ')

        # self.tab_button = QComboBox(self)
        # self.list_tab = ["one", "two", "three"]
        # self.tab_button.addItems(self.list_tab)
        # self.tab_button.currentIndexChanged.connect(lambda state, x= self.tab_button.currentIndex(): self.add_page(x))
        self.tab_button.clicked.connect(self.add_page)
        # self.tab_button.setText()

        self.tab_button.setToolTip("Open a new tab")
        # self.tab_button.setMaximumSize(0, 25)
        # self.corner_widget = QWidget()
        # self.corner_widget.layout = QHBoxLayout(self)
        # self.corner_widget.layout.addStretch(5)
        # self.corner_widget.layout.addWidget(self.tab_button)

        # self.corner_widget.setLayout(self.corner_widget.layout)
        self.tabs.setCornerWidget(self.tab_button)
        # self.tabs.setCornerWidget(self.corner_widget)
        # self.tab_button.clicked.connect(self.add_page)

    def add_page(self):
        # title = self.list_tab[self.tab_button.currentIndex()]
        tab = QWidget()
        tab.layout = QGridLayout(self)
        rec = EmptyTab(self.system_state, self)
        tab.layout.addWidget(rec.table1, 0, 0, 1, 2)
        tab.layout.addWidget(rec.table2, 0, 2, 1, 2)
        tab.layout.addWidget(rec.table3, 1, 0, 1, 3)
        tab.layout.addWidget(rec.table4, 1, 3, 1, 1)
        tab.setLayout(tab.layout)
        # self.tabs.addTab(tab, title)
        self.tabs.addTab(tab, "New Tab")

    def add_tabs(self, tab, title):
        self.tabs.addTab(tab, title)

    def create_tab(self, indice):
        tab = QWidget()
        tab.layout = QGridLayout(self)
        title = self.system_state.data.aspects[indice].aspect_type
        rec = Result(self.system_state, indice, self)

        tab.layout.addWidget(rec.table1, 0, 0, 1, 2)

        tab.layout.addWidget(rec.table2, 0, 2, 1, 2)

        tab.layout.addWidget(rec.table3, 1, 0, 1, 3)  # if i add the buttons directly to Results/createQTable, how do i link them?

        tab.layout.addWidget(rec.table4, 1, 3, 1, 1)

        tab.setLayout(tab.layout)

        self.add_tabs(tab, title)

    # @pyqtSlot()
    # def on_click(self):
    #     print("\n")
    #     for currentQTableWidgetItem in self.tableWidget.selectedItems():
    #         print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
