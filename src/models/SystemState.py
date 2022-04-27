from .Data import *

class SystemState:
    
    modes = ["simple", "expert"]

    def __init__(self):
        self.mode = "simple"  # mode: simple or expert
        self.data = Data()

    def set_mode(self, mode):  # check whether mode in modes?
        self.mode = mode

    def __str__(self):
        s = "\n__System State__\n"
        s += "Mode: " + self.mode

        return s
