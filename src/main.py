import sys
from PyQt5.QtWidgets import QApplication

from views.MainWindow import *
from models.SystemState import *


def main():

    system_state = SystemState()

    app = QApplication(sys.argv)
    window = MainWindow(system_state)
    window.show()
    app.exec_()
    sys.exit()


if __name__ == '__main__':
    main()