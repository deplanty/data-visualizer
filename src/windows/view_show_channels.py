from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QCheckBox, QPushButton
from PySide6.QtCore import Qt


class ViewShowChannelsUI:
    def __init__(self, parent:QWidget, channels):
        layout = QVBoxLayout()
        # Text to explain this window
        label = QLabel("Sélectionner les canaux à afficher :")
        layout.addWidget(label)

        # Add the checkboxes for the channels
        lvb_check = QGridLayout()
        self.checkboxes = list()
        for row, (channel, state) in enumerate(channels, 1):
            label = QLabel(f"Canal {row}:")
            lvb_check.addWidget(label, row, 0)
            checkbox = QCheckBox(channel, parent)
            checkbox.setTristate(False)
            if state:
                checkbox.setCheckState(Qt.Checked)
            else:
                checkbox.setCheckState(Qt.Unchecked)
            lvb_check.addWidget(checkbox, row, 1)
            self.checkboxes.append(checkbox)
        layout.addLayout(lvb_check)

        # Add action buttons
        lhb_buttun = QHBoxLayout()
        self.btn_validate = QPushButton("Valider")
        lhb_buttun.addWidget(self.btn_validate)
        self.btn_cancel = QPushButton("Annuler")
        lhb_buttun.addWidget(self.btn_cancel)
        layout.addLayout(lhb_buttun)

        parent.setLayout(layout)


class ViewShowChannels(QDialog):
    def __init__(self, channels:list[str, bool]):
        super().__init__()

        self.channels = None

        self.ui = ViewShowChannelsUI(self, channels)
        self.ui.btn_validate.clicked.connect(self._on_btn_validate_clicked)
        self.ui.btn_cancel.clicked.connect(self._on_btn_cancel_clicked)

    # Events

    def _on_btn_validate_clicked(self):
        channels = list()
        for check in self.ui.checkboxes:
            channels.append([check.text(), check.checkState() == Qt.Checked])
        self.close()
        self.channels = channels

    def _on_btn_cancel_clicked(self):
        self.close()

    # Methods

    def get(self):
        return self.channels
