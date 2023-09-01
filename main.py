#!venv/Scripts/python


import sys

from PySide6 import QtWidgets

import src.preload
from src.frames import MainWindow



class Application(QtWidgets.QApplication):
    def __init__(self, argv:list):
        super().__init__(argv)
        self.window = MainWindow()

    def run(self):
        """
        Main method to run the application

        Returns:
            int: exit code
        """

        self.window.show()
        return self.exec()


if __name__ == '__main__':
    # Start application
    app = Application(sys.argv)
    sys.exit(app.run())
