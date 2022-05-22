from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from .DropMenu import *
from models.Aspect import *
from fusion import *


class Aspects(QWidget):

    def __init__(self, controller, parent=None):

        super(Aspects, self).__init__(parent)

        self.parent = parent
        self.controller = controller

        self.drop_menu_list = []

        self.layout = QGridLayout(self)

        self.add_aspect_btn = QPushButton(" + ")
        self.add_aspect_btn.setMinimumSize(40, 40)
        # self.add_aspect_btn.setMinimumSize(60, 60)
        self.add_aspect_btn.setMaximumSize(60, 40)
        self.add_aspect_btn.clicked.connect(self.add_aspect)
        self.layout.addWidget(self.add_aspect_btn, 0, 1)

        self.add_aspect()

    def add_aspect(self):
        # Add an aspect
        aspect_id = self.controller.add_empty_aspect()

        l = len(self.drop_menu_list)
        new_drop_menu = DropMenu(self.controller, aspect_id, self.remove_aspect, parent=self)
        self.drop_menu_list.append(new_drop_menu)

        if l == 0:
            self.add_aspect_btn.setText(" + ")
            self.add_aspect_btn.setMinimumSize(40, 40)
            # self.add_aspect_btn.setMaximumSize(60, 60)

        self.layout.addWidget(self.drop_menu_list[-1], 1, l)
        self.layout.addWidget(self.add_aspect_btn, 0, l+1)

    def remove_aspect(self, widg):
        # Remove the aspect from the display
        self.layout.removeWidget(widg)

        # Remove the aspect from the list
        place = self.drop_menu_list.index(widg)
        self.drop_menu_list.remove(widg)

        for k in range(place, len(self.drop_menu_list)):
            self.layout.addWidget(self.drop_menu_list[k], 1, k)

        l = len(self.drop_menu_list)
        self.layout.addWidget(self.add_aspect_btn, 0, l)

        if l == 0:
            self.add_aspect_btn.setText("New aspect")
            self.add_aspect_btn.setMaximumSize(300, 60)
        widg.deleteLater()
