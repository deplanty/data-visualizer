#!venv/Scripts/python

import sys

from PySide6 import QtWidgets

import src.preload
from src import logger
from src.frames import MainWindow


class Application(QtWidgets.QApplication):
    def __init__(self, argv: list):
        super().__init__(argv)
        self.window = MainWindow()

    def run(self):
        """
        Main method to run the application

        Returns:
            int: exit code
        """

        logger.debug("Start application")
        self.window.show()
        return self.exec()


if __name__ == "__main__":
    # Start application
    app = Application(sys.argv)
    code = app.run()
    logger.debug(f"Stop application with code {code}")
    sys.exit(code)
