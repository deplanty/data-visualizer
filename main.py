#!venv/Scripts/python

import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

import src.preload as pl
from src import logger
from src.frames import MainWindow


class Application(QApplication):
    def __init__(self, argv: list):
        super().__init__(argv)
        self.window = MainWindow()
        # Setup the window state from the settings
        if pl.settings.get("application/maximized"):
            self.window.setWindowState(Qt.WindowState.WindowMaximized)

        self.aboutToQuit.connect(self._on_about_to_quit)

    # Events

    def _on_about_to_quit(self):
        maximized = self.window.windowState() == Qt.WindowState.WindowMaximized
        pl.settings.set("application/maximized", maximized)

    # Methods

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
