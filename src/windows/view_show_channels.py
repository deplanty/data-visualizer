from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QCheckBox, QPushButton, QColorDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from src.objects import DataContainer


class ViewShowChannelsUI:
    def __init__(self, parent:QWidget, channels):
        layout = QVBoxLayout()
        # Text to explain this window
        label = QLabel("Sélectionner les canaux à afficher :")
        layout.addWidget(label)

        # Add the checkboxes for the channels
        lg_check = QGridLayout()
        self.checkboxes = list()
        self.buttons = list()
        for row, channel in enumerate(channels.y, 1):
            label = QLabel(f"Canal {row}:")
            lg_check.addWidget(label, row, 0)
            checkbox = QCheckBox(channel.label, parent)
            checkbox.setTristate(False)
            checkbox.setCheckState(Qt.Checked if channel.show else Qt.Unchecked)
            lg_check.addWidget(checkbox, row, 1)
            button = QPushButton()
            self.buttons.append(button)
            lg_check.addWidget(button, row, 2)
            self.checkboxes.append(checkbox)
        layout.addLayout(lg_check)

        # Add action buttons
        lhb_buttun = QHBoxLayout()
        self.btn_validate = QPushButton("Valider")
        lhb_buttun.addWidget(self.btn_validate)
        self.btn_cancel = QPushButton("Annuler")
        lhb_buttun.addWidget(self.btn_cancel)
        layout.addLayout(lhb_buttun)

        parent.setLayout(layout)


class ViewShowChannels(QDialog):
    def __init__(self, data:DataContainer):
        super().__init__()

        self.data = data
        self._changed = False

        self.ui = ViewShowChannelsUI(self, data)
        for i, button in enumerate(self.ui.buttons):
            button.clicked.connect(lambda: self._on_btn_color_select_clicked_for(i))
        self.ui.btn_validate.clicked.connect(self._on_btn_validate_clicked)
        self.ui.btn_cancel.clicked.connect(self._on_btn_cancel_clicked)

    # Events

    def _on_btn_validate_clicked(self):
        for check, y in zip(self.ui.checkboxes, self.data.y):
            y.set(show=check.checkState() == Qt.Checked)

        self._changed = True
        self.close()

    def _on_btn_cancel_clicked(self):
        self._changed = False
        self.close()

    def _on_btn_color_select_clicked_for(self, index:int):
        dialog = QColorDialog()
        dialog.setCurrentColor(QColor(*self._to_int_color(self.data.y[index].color)))
        dialog.exec()
        color = dialog.selectedColor()
        if color.isValid():
            self.data.y[index].color = self._to_float_color(color.toTuple())

    # Methods

    def has_changed(self):
        return self._changed

    def _to_int_color(self, color:list):
        return [int(x * 255) for x in color]

    def _to_float_color(self, color:list):
        return [x / 255 for x in color]
