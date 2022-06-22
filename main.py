import sys

from PyQt5 import QtWidgets

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
        return self.exec_()


if __name__ == '__main__':
    # Start application
    app = Application(sys.argv)
    exit_code = app.run()
    sys.exit(exit_code)
