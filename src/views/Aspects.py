from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from .DropMenu import *
from models.Aspect import *

class Aspects(QWidget):

    def __init__(self, system_state, parent=None):

        super(Aspects, self).__init__(parent)

        self.parent = parent
        self.system_state = system_state

        self.drop_menu_list = []
        self.remove_btns = []

        self.dropmenu = DropMenu(parent=self)
        new_btn = QPushButton("-", self)
        self.remove_btns.append(new_btn)
        new_btn.setEnabled(False)
        new_btn.setMaximumSize(35, 25)

        self.drop_menu_list.append(self.dropmenu)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.dropmenu, 1, 0)
        self.layout.addWidget(new_btn, 0, 0, alignment=Qt.AlignRight)

        self.add_aspect_btn = QPushButton("Add an aspect", self)
        self.calc_btn = QPushButton("Calculate", self)
        self.calc_btn.setEnabled(False)

        self.layout.addWidget(self.add_aspect_btn, 2, 2)
        self.layout.addWidget(self.calc_btn, 2, 3)

        self.add_aspect_btn.clicked.connect(self.add_aspect)
        self.calc_btn.clicked.connect(self.calculate)
        new_btn.clicked.connect(lambda state, x=0: self.remove_aspect(x))

    def add_aspect(self):
        self.calc_btn.setEnabled(False)
        # Add an aspect
        l = len(self.drop_menu_list)
        new_drop_menu = DropMenu(parent=self)
        self.drop_menu_list.append(new_drop_menu)

        new_btn = QPushButton("-", self)
        new_btn.setMaximumSize(35, 25)
        # Connect the "-" button to remove this aspect
        new_btn.clicked.connect(lambda state, x=l: self.remove_aspect(x))
        self.remove_btns.append(new_btn)

        # Enable the remove buttons if there's more than one aspect
        for b in self.remove_btns:
            b.setEnabled(len(self.drop_menu_list) > 1)

        curr = len(self.drop_menu_list)
        self.layout.addWidget(self.drop_menu_list[-1], 1, l)
        self.layout.addWidget(new_btn, 0, l, alignment=Qt.AlignRight)

    def remove_aspect(self, i):
        # TODO: liste des colonnes (one widget)
        del_menu = self.drop_menu_list[i]
        # Remove the aspect from the display
        self.layout.removeWidget(del_menu)
        self.layout.removeWidget(self.remove_btns[i])
        for k in range(len(self.drop_menu_list)):
            print(self.drop_menu_list[k])
        # Remove the aspect from the list
        self.drop_menu_list.pop(i)
        self.remove_btns.pop(i)

        # Enable the remove buttons if there's more than one aspect
        for b in self.remove_btns:
            b.setEnabled(len(self.drop_menu_list) > 1)

        self.check()

    def check(self):
        # checks whether all menus are filled to enable the calculate button

        all_filled = True
        # Can't calculate if all items have not been selected
        for aspect_menu in self.drop_menu_list:
            if aspect_menu.filled == False:
                all_filled = False

        self.calc_btn.setEnabled(all_filled)  

        # # Check if any aspects selected are the same
        # ok = True
        # for i in range(len(self.drop_menu_list)):
        #     for j in range(i, len(self.drop_menu_list)):
        #         if i == j:
        #             continue
        #         if self.Aspects[i] == self.Aspects[j]:
        #             # put the aspects in red and pop up a qlabel
        #             print(f"Aspects {i} and {j} must be different from each other!")
        #             ok = False
        # return ok

    def calculate(self):
        # if not self.check():
        #     print("Can't calculate, all aspects are not different.")
        #     return
        print("Calculating...")

        # Creating the Aspects objects and putting them in a list
        for drop_menu in self.drop_menu_list:
            a = Aspect.create_from_csv(drop_menu.aspect_type, drop_menu.users_file, drop_menu.activities_file, (0, 5), (0, 5))
            self.system_state.data.add_aspect(a)

        self.parent.set_page_results()

    def create_aspect_object(self, drop_menu):
        # print(drop_menu.aspect, drop_menu.user, drop_menu.activity)
        
        return a
