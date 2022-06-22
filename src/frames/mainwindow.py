from PyQt5 import QtWidgets

from .mainwindow_ui import MainWindowUI


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = MainWindowUI(self)

        self.ui.menu_file_exit.triggered.connect(self._on_menu_file_exit_triggered)

    # Events

    def _on_menu_file_exit_triggered(self):
        self.close()
