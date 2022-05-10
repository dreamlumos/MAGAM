import sys
from PyQt5.QtWidgets import QApplication

from views.MainWindow import *
from models.SystemState import *


def main():

    system_state = SystemState()

    app = QApplication(sys.argv)
    window = MainWindow(system_state)

    # labels = dict()
    # style = ""
    # with open("style.qss", "r") as style_sheet:
    #     style = style_sheet.read()

    # with open("colourcodes.txt", "r") as colour_codes:
    #     text = colour_codes.readlines()
    #     for line in text:
    #         key, value = line.strip().split()
    #         labels.update({key: value})
    # print(labels)

    # for key, value in labels.items():
    #     style = style.replace(key, value)
    # print(style)

    with open("style.qss", "r") as s:
        style = s.read()

    window.setStyleSheet(style)
    window.show()
    app.exec_()
    sys.exit()


if __name__ == '__main__':
    main()