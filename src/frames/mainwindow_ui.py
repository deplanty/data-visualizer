from PyQt5 import QtWidgets

from src.tools import MplCanvas


class MainWindowUI():
    def __init__(self, master:QtWidgets):
        self.master = master

        self.master.setWindowTitle("Data visualizer")
        self.master.resize(800, 600)

        menubar = self.master.menuBar()
        menu_file = menubar.addMenu("Fichier")
        self.menu_file_open = QtWidgets.QAction("Ouvrir...", self.master)
        self.menu_file_open.setShortcut("Ctrl+o")
        menu_file.addAction(self.menu_file_open)
        # self.menu_file_save = QtWidgets.QAction("Sauvegarder", self.master)
        # self.menu_file_save.setShortcut("Ctrl+s")
        # menu_file.addAction(self.menu_file_save)
        # self.menu_file_saveas = QtWidgets.QAction("Sauvegarder sous...", self.master)
        # self.menu_file_saveas.setShortcut("Ctrl+Shift+s")
        # menu_file.addAction(self.menu_file_saveas)
        self.menu_file_exit = QtWidgets.QAction("Quitter", self.master)
        self.menu_file_exit.setShortcut("Ctrl+q")
        menu_file.addAction(self.menu_file_exit)


        frame = QtWidgets.QWidget(self.master)
        self.master.setCentralWidget(frame)

        self.layout_h = QtWidgets.QHBoxLayout(frame)
        self.layout_buttons = QtWidgets.QVBoxLayout(frame)
        self.combo_analyze_1 = QtWidgets.QComboBox(frame)
        self.combo_analyze_2 = QtWidgets.QComboBox(frame)
        self.combo_analyze_3 = QtWidgets.QComboBox(frame)
        self.combo_analyze_4 = QtWidgets.QComboBox(frame)
        self.combo_analyze_5 = QtWidgets.QComboBox(frame)
        self.layout_buttons.addWidget(self.combo_analyze_1)
        self.layout_buttons.addWidget(self.combo_analyze_2)
        self.layout_buttons.addWidget(self.combo_analyze_3)
        self.layout_buttons.addWidget(self.combo_analyze_4)
        self.layout_buttons.addWidget(self.combo_analyze_5)
        self.layout_h.addLayout(self.layout_buttons, 1)
        self.layout_h.addWidget(MplCanvas(frame), 5)
        frame.setLayout(self.layout_h)

        for c in [self.combo_analyze_1, self.combo_analyze_2, self.combo_analyze_3, self.combo_analyze_4, self.combo_analyze_5]:
            c.addItem("Min")
            c.addItem("Max")
            c.addItem("Delta T")
            c.addItem("Pic-Pic")
            c.addItem("Integrale")
