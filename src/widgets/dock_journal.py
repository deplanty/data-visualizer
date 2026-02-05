from PySide6.QtWidgets import QWidget, QDockWidget, QLabel, QVBoxLayout, QTextEdit
from PySide6.QtCore import Qt


class DockJournalUi:
    def __init__(self, widget: QDockWidget):
        widget.setWindowTitle("Console")
        widget.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        widget.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable
            | QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )

        self.text_edit = QTextEdit()
        widget.setWidget(self.text_edit)


class DockJournal(QDockWidget):
    def __init__(self):
        super().__init__()

        self.ui = DockJournalUi(self)

    def log(self, text: str):
        self.ui.text_edit.insertPlainText(text + "\n")
