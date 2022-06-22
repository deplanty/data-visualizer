from PyQt5 import QtWidgets
from PyQt5 import QtGui

from src.tools import MplCanvas


class MainWindowUI():
    def __init__(self, master:QtWidgets):
        self.master = master

        self.master.setWindowTitle("Data visualizer")
        self.master.resize(800, 600)

        frame = QtWidgets.QWidget(self.master)
        self.master.setCentralWidget(frame)

        self.layout_h = QtWidgets.QHBoxLayout(frame)
        self.layout_buttons = QtWidgets.QVBoxLayout(frame)
        self.layout_buttons.addWidget(QtWidgets.QPushButton("Button 1"))
        self.layout_buttons.addWidget(QtWidgets.QPushButton("Button 2"))
        self.layout_buttons.addWidget(QtWidgets.QPushButton("Button 3"))
        self.layout_h.addLayout(self.layout_buttons, 1)
        self.layout_h.addWidget(MplCanvas(frame), 5)
        frame.setLayout(self.layout_h)
