import PyQt5.QtBluetooth
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .Aspects import *
from .Result import *
from .AspectTab import *
from .FusionTab import *
from models.Aspect import *
from PyQt5.QtCore import *
from functools import partial


class TabContainer(QWidget):

    def __init__(self, controller, parent=None):
        super(TabContainer, self).__init__(parent)

        self.controller = controller

        self.layout = QHBoxLayout(self)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(lambda index: self.tabs.removeTab(index))

        # self.main_menu = QWidget()
        # self.main_menu.layout = QHBoxLayout(self)
        # qtable = QTableWidget(1000, 1000, self)
        # self.main_menu.layout.addWidget(qtable)
        # self.main_menu.setLayout(self.main_menu.layout)
        # self.tabs.addTab(self.main_menu, "Main Menu")

        self.tabs.addTab(Aspects(controller, self), "Overview")
        self.tabs.tabBar().setTabButton(0, QTabBar.RightSide, None)

        # TODO add csv button
        # TODO add recalculate button

        self.tabs.addTab(FusionTab(self.controller, self), "Fusion")  # Fusion
        self.tabs.tabBar().setTabButton(1, QTabBar.RightSide, None)

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

    def add_page(self, aspect_type=None, users_qtable=None, activities_qtable=None, recommendations_qtable=None, function=None):
        
        aspect_id = self.controller.add_empty_aspect()
        tab = AspectTab(self.controller, aspect_id, aspect_type, users_qtable, activities_qtable, recommendations_qtable, function, self)
        # users_qtable.resizeColumnsToContents()
        # activities_qtable.resizeColumnsToContents()
        # recommendations_qtable.resizeColumnsToContents()
        title = ""
        if aspect_type == None or aspect_type == False:
            title = "New Tab"
        else:
            title = aspect_type
        tab_index = self.tabs.addTab(tab, title)
        tab.set_index(tab_index)

        # self.tabs.addTab(splitter, "New Tab")

        # splitter = QSplitter(Qt.Vertical)
        # tab = EmptyTab(self.controller, self)
        #
        # widg1 = QWidget()
        # widg1.layout = QHBoxLayout()
        # widg1.layout.addWidget(tab.table1)
        # widg1.layout.addWidget(tab.table2)
        # widg1.setLayout(widg1.layout)
        #
        # widg2 = QFrame()
        # widg2.layout = QHBoxLayout()
        # widg2.layout.addWidget(tab.table3)
        # widg2.layout.addWidget(tab.table4)
        # widg2.setLayout(widg2.layout)
        #
        # splitter.addWidget(widg1)
        # splitter.addWidget(QTextEdit())
        # splitter.setSizes([100, 200])
        # self.tabs.addTab(splitter, "split")

    def create_tab(self, indice):
        tab = QWidget()
        tab.layout = QGridLayout(self)
        title = self.controller.data.aspects[indice].aspect_type
        tab = Result(self.controller, indice, self)

        tab.layout.addWidget(tab.table1, 0, 0, 1, 2)

        tab.layout.addWidget(tab.table2, 0, 2, 1, 2)

        tab.layout.addWidget(tab.table3, 1, 0, 1, 3)  # if i add the buttons directly to Results/createQTable, how do i link them?

        tab.layout.addWidget(tab.table4, 1, 3, 1, 1)

        tab.setLayout(tab.layout)

        self.add_tabs(tab, title)

    # @pyqtSlot()
    # def on_click(self):
    #     print("\n")
    #     for currentQTableWidgetItem in self.tableWidget.selectedItems():
    #         print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
