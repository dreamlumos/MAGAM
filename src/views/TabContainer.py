import PyQt5.QtBluetooth
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .Aspects import *
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

        self.tabs.addTab(Aspects(controller, self), "Overview")
        self.tabs.tabBar().setTabButton(0, QTabBar.RightSide, None)

        self.tabs.addTab(FusionTab(self.controller, self), "Fusion")  # Fusion
        self.tabs.tabBar().setTabButton(1, QTabBar.RightSide, None)

        self.tab_button = QPushButton(self)
        self.tab_button.setText(' + ')
        self.tab_button.clicked.connect(self.add_page)

        self.tab_button.setToolTip("Open a new blank tab")

        self.tabs.setCornerWidget(self.tab_button)

    def add_page(self, aspect_type=None, users_qtable=None, activities_qtable=None, recommendations_qtable=None,
                 function=None):

        aspect_id = self.controller.add_empty_aspect()
        tab = AspectTab(self.controller, aspect_id, aspect_type, users_qtable, activities_qtable, recommendations_qtable, function, self)

        title = ""
        if aspect_type is None or aspect_type is False:
            title = "New Tab"
        else:
            title = aspect_type
        # tab_index = self.tabs.addTab(tab, title)
        curr_index = self.tabs.count()
        tab_index = self.tabs.insertTab(curr_index - 1, tab, title)
        tab.set_index(tab_index)

    def create_tab(self, indice):
        tab = QWidget()
        tab.layout = QGridLayout(self)
        title = self.controller.data.aspects[indice].aspect_type
        tab = Result(self.controller, indice, self)

        tab.layout.addWidget(tab.table1, 0, 0, 1, 2)

        tab.layout.addWidget(tab.table2, 0, 2, 1, 2)

        tab.layout.addWidget(tab.table3, 1, 0, 1, 3)

        tab.layout.addWidget(tab.table4, 1, 3, 1, 1)

        tab.setLayout(tab.layout)

        self.add_tabs(tab, title)
