from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class WindowJournalUi:
    def __init__(self, widget: QWidget):
        widget.setWindowTitle("Data visualizer - Journal")

        layout = QVBoxLayout()
        label = QLabel()
        label.setText("Journal de bord")
        layout.addWidget(label)
        widget.setLayout(layout)


class WindowJournal(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = WindowJournalUi(self)
