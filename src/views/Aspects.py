from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from .DropMenu import *
from models.Aspect import *
from src.fusion import *
from .Results import *


class Aspects(QWidget):

    def __init__(self, system_state, parent=None):

        super(Aspects, self).__init__(parent)

        self.parent = parent
        self.system_state = system_state

        self.drop_menu_list = []
        # self.remove_btns = []
        self.fusion = FusionFunctions.functions[0]  # by default for now

        self.dropmenu = DropMenu(self.remove_aspect, parent=self)
        # new_btn = QPushButton("- 0", self)
        # self.remove_btns.append(new_btn)
        # new_btn.setEnabled(False)
        # new_btn.setMaximumSize(35, 25)

        self.drop_menu_list.append(self.dropmenu)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.dropmenu, 1, 0)
        # self.layout.addWidget(new_btn, 0, 0, alignment=Qt.AlignRight)

        self.add_aspect_btn = QPushButton("Add an aspect", self)
        self.calc_btn = QPushButton("Calculate", self)
        self.calc_btn.setEnabled(False)
        self.pick_fusion = QComboBox()
        # self.pick_calc_btn.addItems(["------"])
        self.pick_fusion.addItems(FusionFunctions.functions)

        self.layout.addWidget(self.add_aspect_btn, 2, 2)
        self.layout.addWidget(self.calc_btn, 2, 3)
        self.layout.addWidget(QLabel("Fusion Function"), 0, 3)
        self.layout.addWidget(self.pick_fusion, 1, 3)

        self.add_aspect_btn.clicked.connect(self.add_aspect)
        # self.calc_btn.clicked.connect(self.calculate)
        self.calc_btn.clicked.connect(self.confirm_calcul)
        self.pick_fusion.currentIndexChanged.connect(self.fusion_picked)
        # new_btn.clicked.connect(lambda state, x=self.remove_btns.index(new_btn): self.remove_aspect(x))

    def add_aspect(self):
        print("len of menu : ", len(self.drop_menu_list))
        print(self.drop_menu_list)
        # print("len of remove btns : ", len(self.remove_btns))

        self.calc_btn.setEnabled(False)
        # Add an aspect
        l = len(self.drop_menu_list)
        new_drop_menu = DropMenu(self.remove_aspect, parent=self)
        self.drop_menu_list.append(new_drop_menu)
        #
        # new_btn = QPushButton(f"- {len(self.drop_menu_list)-1}", self)
        # new_btn.setMaximumSize(35, 25)
        # Connect the "-" button to remove this aspect
        # self.remove_btns.append(new_btn)
        # new_btn.clicked.connect(lambda state, x=self.remove_btns.index(new_btn): self.remove_aspect(x))

        # Enable the remove buttons if there's more than one aspect
        # for b in self.remove_btns:
        #     b.setEnabled(len(self.drop_menu_list) > 1)

        curr = len(self.drop_menu_list)
        self.layout.addWidget(self.drop_menu_list[-1], 1, l)
        # self.layout.addWidget(new_btn, 0, l, alignment=Qt.AlignRight)

    def remove_aspect(self, widg):
        print("len of menu : ", len(self.drop_menu_list))
        # print("len of remove btns : ", len(self.remove_btns))
        # del_menu = self.drop_menu_list[i]
        # Remove the aspect from the display
        if len(self.drop_menu_list) <= 1:
            return
        self.layout.removeWidget(widg)
        # self.layout.removeWidget(self.remove_btns[i])
        for k in range(len(self.drop_menu_list)):
            print(self.drop_menu_list[k])
        # Remove the aspect from the list
        print(self.drop_menu_list)
        print(widg)
        self.drop_menu_list.remove(widg)
        widg.deleteLater()
        print(self.drop_menu_list)
        # self.remove_btns.pop(i)
        print("len of menu : ", len(self.drop_menu_list))
        # print("len of remove btns : ", len(self.remove_btns))

        # Enable the remove buttons if there's more than one aspect
        # for b in self.remove_btns:
        #     b.setEnabled(len(self.drop_menu_list) > 1)

        self.check()

    def fusion_picked(self):
        self.fusion = self.pick_fusion.currentText()

    def check(self):
        # checks whether all menus are filled to enable the calculate button

        all_filled = True
        # Can't calculate if all items have not been selected
        for aspect_menu in self.drop_menu_list:
            if not aspect_menu.filled:
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

    def confirm_calcul(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Calculation")
        s = ""
        for i in range(len(self.drop_menu_list)):
            s += "Function '" + self.drop_menu_list[i].function + "' for the " + self.drop_menu_list[i].aspect_type + \
                 " aspect\n"
        msg.setText(f"Fusion function {self.fusion} will be used on:\n" + s)

        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        msg.show()
        res = msg.exec()
        if res == QMessageBox.Ok:
            self.calculate()

    def calculate(self):
        # if not self.check():
        #     print("Can't calculate, all aspects are not different.")
        #     return

        # msg.setDefaultButton(QMessageBox.Retry)
        # msg.setInformativeText("informative text, ya!")
        # msg.setDetailedText("details")
        # msg.buttonClicked.connect(self.popup_button)
        print("Calculating...")

        # Creating the Aspects objects and putting them in a list
        for drop_menu in self.drop_menu_list:
            print(drop_menu.function)
            a = Aspect.create_from_csv(drop_menu.aspect_type, drop_menu.users_file, (0, 5), drop_menu.activities_file, (0, 5), drop_menu.function)
            self.system_state.data.add_aspect(a)
        # self.parent.set_page_results()
        self.results_widget = Results(self.system_state, self)
        self.layout.addWidget(self.results_widget, 2, 0)

    # def create_aspect_object(self, drop_menu):
    #     # print(drop_menu.aspect, drop_menu.user, drop_menu.activity)
    #
    #     return a
