from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QGridLayout,
    QComboBox,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QVBoxLayout,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from src.objects import DataAnalyzer

from .mpl_canvas import MplCanvas


class MainWindowUI:
    def __init__(self, master: QMainWindow):
        self.master = master

        self.master.setWindowTitle("Data visualizer")
        self.master.resize(800, 600)

        # Top menu
        menubar = self.master.menuBar()
        # File
        menu_file = menubar.addMenu("File")
        self.menu_file_open = QAction("Open...")
        self.menu_file_open.setShortcut("Ctrl+o")
        menu_file.addAction(self.menu_file_open)
        # self.menu_file_save = QAction("Save", self.master)
        # self.menu_file_save.setShortcut("Ctrl+s")
        # menu_file.addAction(self.menu_file_save)
        self.menu_file_saveselectionas = QAction("Save selection as...", self.master)
        menu_file.addAction(self.menu_file_saveselectionas)
        # self.menu_file_saveas = QAction("Save as...", self.master)
        # self.menu_file_saveas.setShortcut("Ctrl+Shift+s")
        # menu_file.addAction(self.menu_file_saveas)
        self.menu_file_exit = QAction("Quit")
        self.menu_file_exit.setShortcut("Ctrl+q")
        menu_file.addAction(self.menu_file_exit)
        # View
        menu_view = menubar.addMenu("View")
        self.menu_view_show_channels = QAction("Channels settings...")
        menu_view.addAction(self.menu_view_show_channels)
        # Scripts
        self.menu_scripts = menubar.addMenu("Scripts")
        self.menu_scripts_list = list()

        # Main widget
        frame = QWidget()
        self.master.setCentralWidget(frame)

        # Fill the main widget
        self.layout_h = QHBoxLayout()
        self.layout_grid = QGridLayout()
        # self.layout_grid.setVerticalSpacing(0)

        self.grid = list()
        for i in range(5):
            # Mesure function to use
            combo_measure = QComboBox()
            combo_measure.setFixedWidth(100)
            self.layout_grid.addWidget(combo_measure, i, 0)
            # On which channel the measure is done
            combo_channel = QComboBox()
            combo_channel.setFixedWidth(40)
            self.layout_grid.addWidget(combo_channel, i, 1)
            # Result of the measure
            label = QLabel()
            label.setFixedWidth(60)
            self.layout_grid.addWidget(label, i, 2)
            self.grid.append({"measure": combo_measure, "channel": combo_channel, "label": label})
        # Space to put the rows on top of the widget
        verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.layout_grid.addItem(verticalSpacer, 5, 0)

        # Graph and navigation toolbox
        self.layout_h.addLayout(self.layout_grid, 1)
        self.layout_v_graph = QVBoxLayout()
        self.mpl_canvas = MplCanvas()
        self.layout_v_graph.addWidget(self.mpl_canvas)
        self.layout_v_graph.addWidget(self.mpl_canvas.toolbar)  # type: ignore
        self.layout_h.addLayout(self.layout_v_graph, 5)
        frame.setLayout(self.layout_h)

        # Add the parameters in the comboboxes
        for row in self.grid:
            c = row["measure"]
            for name in DataAnalyzer.list_all():
                c.addItem(name)

            c = row["channel"]
            c.addItem("1")

    def set_channels(self, n_channels: int):
        for row in self.grid:
            c = row["channel"]
            c.clear()
            c.addItems(str(i + 1) for i in range(n_channels))

    def add_script_menu(self, name: str):
        menu = QAction(name)
        self.menu_scripts.addAction(menu)
        self.menu_scripts_list.append(menu)
        return menu
