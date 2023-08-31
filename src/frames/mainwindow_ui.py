from PySide6 import QtWidgets
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from src.objects.enums import AnalyseType

from .mpl_canvas import MplCanvas


class MainWindowUI():
    def __init__(self, master:QtWidgets):
        self.master = master

        self.master.setWindowTitle("Data visualizer")
        self.master.resize(800, 600)

        # Top menu
        menubar = self.master.menuBar()
        menu_file = menubar.addMenu("File")
        self.menu_file_open = QAction("Open...")
        self.menu_file_open.setShortcut("Ctrl+o")
        menu_file.addAction(self.menu_file_open)
        # self.menu_file_save = QAction("Save", self.master)
        # self.menu_file_save.setShortcut("Ctrl+s")
        # menu_file.addAction(self.menu_file_save)
        # self.menu_file_saveas = QAction("Save as...", self.master)
        # self.menu_file_saveas.setShortcut("Ctrl+Shift+s")
        # menu_file.addAction(self.menu_file_saveas)
        self.menu_file_exit = QAction("Quit")
        self.menu_file_exit.setShortcut("Ctrl+q")
        menu_file.addAction(self.menu_file_exit)

        menu_view = menubar.addMenu("View")
        self.menu_view_show_channels = QAction("Channels settings...")
        menu_view.addAction(self.menu_view_show_channels)

        # Main widget
        frame = QtWidgets.QWidget()
        self.master.setCentralWidget(frame)

        # Fill the main widget
        self.layout_h = QtWidgets.QHBoxLayout()
        self.layout_grid = QtWidgets.QGridLayout()
        # self.layout_grid.setVerticalSpacing(0)

        self.grid = list()
        for i in range(5):
            combo_measure = QtWidgets.QComboBox()
            self.layout_grid.addWidget(combo_measure, i, 0)
            combo_channel = QtWidgets.QComboBox()
            self.layout_grid.addWidget(combo_channel, i, 1)
            label = QtWidgets.QLabel()
            label.setFixedWidth(50)
            self.layout_grid.addWidget(label, i, 2)
            self.grid.append({
                "measure": combo_measure,
                "channel": combo_channel,
                "label": label
            })
        verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout_grid.addItem(verticalSpacer, i + 1, 0)

        self.layout_h.addLayout(self.layout_grid, 1)
        self.layout_v_graph = QtWidgets.QVBoxLayout()
        self.mpl_canvas = MplCanvas()
        self.layout_v_graph.addWidget(self.mpl_canvas)
        self.layout_v_graph.addWidget(self.mpl_canvas.toolbar)
        self.layout_h.addLayout(self.layout_v_graph, 5)
        frame.setLayout(self.layout_h)

        for row in self.grid:
            c = row["measure"]
            for name in AnalyseType.list_all():
                c.addItem(name)

            c = row["channel"]
            c.addItem("1")

    def set_channels(self, n_channels:int):
        for row in self.grid:
            c = row["channel"]
            c.clear()
            c.addItems(str(i + 1) for i in range(n_channels))
