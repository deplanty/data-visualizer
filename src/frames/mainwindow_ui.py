from PySide6 import QtWidgets
from PySide6.QtGui import QAction

from src.tools import MplCanvas


class MainWindowUI():
    def __init__(self, master:QtWidgets):
        self.master = master

        self.master.setWindowTitle("Data visualizer")
        self.master.resize(800, 600)

        menubar = self.master.menuBar()
        menu_file = menubar.addMenu("Fichier")
        self.menu_file_open = QAction("Ouvrir...", self.master)
        self.menu_file_open.setShortcut("Ctrl+o")
        menu_file.addAction(self.menu_file_open)
        # self.menu_file_save = QAction("Sauvegarder", self.master)
        # self.menu_file_save.setShortcut("Ctrl+s")
        # menu_file.addAction(self.menu_file_save)
        # self.menu_file_saveas = QAction("Sauvegarder sous...", self.master)
        # self.menu_file_saveas.setShortcut("Ctrl+Shift+s")
        # menu_file.addAction(self.menu_file_saveas)
        self.menu_file_exit = QAction("Quitter", self.master)
        self.menu_file_exit.setShortcut("Ctrl+q")
        menu_file.addAction(self.menu_file_exit)


        frame = QtWidgets.QWidget(self.master)
        self.master.setCentralWidget(frame)

        self.layout_h = QtWidgets.QHBoxLayout(frame)
        self.layout_grid = QtWidgets.QGridLayout(frame)

        self.grid = list()
        for i in range(5):
            combo_measure = QtWidgets.QComboBox(frame)
            self.layout_grid.addWidget(combo_measure, i, 0)
            combo_channel = QtWidgets.QComboBox(frame)
            self.layout_grid.addWidget(combo_channel, i, 1)
            label = QtWidgets.QLabel(frame)
            self.layout_grid.addWidget(label, i, 2)
            self.grid.append({
                "measure": combo_measure,
                "channel": combo_channel,
                "label": label
            })

        self.layout_h.addLayout(self.layout_grid, 1)
        self.mpl_canvas = MplCanvas(frame)
        self.layout_h.addWidget(self.mpl_canvas, 5)
        frame.setLayout(self.layout_h)

        for row in self.grid:
            c = row["measure"]
            c.addItem("Minimum")
            c.addItem("Maximum")
            c.addItem("Mean")
            c.addItem("Delta T")
            c.addItem("Pic-Pic")
            c.addItem("Integrale")

            c = row["channel"]
            c.addItem("1")

    def set_channels(self, n_channels:int):
        for row in self.grid:
            c = row["channel"]
            c.clear()
            c.addItems(str(i + 1) for i in range(n_channels))
