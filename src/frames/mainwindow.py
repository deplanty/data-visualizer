from PyQt5 import QtWidgets

from .mainwindow_ui import MainWindowUI


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = MainWindowUI(self)
