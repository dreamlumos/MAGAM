import sys
from PyQt5.QtWidgets import QApplication

from views.MainWindow import *
from models.SystemState import *
from Controller import *


def main():
    system_state = SystemState()
    controller = Controller(system_state)

    app = QApplication(sys.argv)
    gui = MainWindow(controller)

    with open("style.qss", "r") as s:
        style = s.read()

    gui.setStyleSheet(style)
    gui.show()
    app.exec_()
    sys.exit()


if __name__ == '__main__':
    main()
