import sys
from PyQt5.QtWidgets import QApplication

from views.MainWindow import *

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
    sys.exit()


if __name__ == '__main__':
    main()