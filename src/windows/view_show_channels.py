from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel, QCheckBox, QPushButton, QColorDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from src.objects import DataContainer
from src.tools import colors


class ViewShowChannelsUI:
    def __init__(self, parent:QWidget, channels):
        parent.setWindowTitle("Data visualizer - Channels")

        layout = QVBoxLayout()
        # Text to explain this window
        group_box = QGroupBox("Configure channels settings:")
        layout.addWidget(group_box)

        layout_group = QVBoxLayout()

        # Add the parameters for the channels
        grid_layout_settings = QGridLayout()
        self.checkboxes = list()
        self.buttons = list()
        self.l_colors = list()
        # Add header or this grid
        label = QLabel("Display curve")
        grid_layout_settings.addWidget(label, 0, 1)
        label = QLabel("Curve color")
        grid_layout_settings.addWidget(label, 0, 2)
        for row, channel in enumerate(channels.y, 1):
            # Label for the channel number
            label = QLabel(f"Channel {row}:")
            grid_layout_settings.addWidget(label, row, 0)
            # Checkbox with the channel name
            checkbox = QCheckBox(channel.label)
            checkbox.setTristate(False)
            checkbox.setCheckState(Qt.Checked if channel.show else Qt.Unchecked)
            grid_layout_settings.addWidget(checkbox, row, 1)
            self.checkboxes.append(checkbox)
            # Button to change the curve color
            button = QPushButton()
            lay = QHBoxLayout()
            self.buttons.append(button)
            grid_layout_settings.addWidget(button, row, 2)
            # Display the current color in the button
            # This is not very elegant, but it works
            l_color = QLabel()
            l_color.setFixedWidth(25)
            self.l_colors.append(l_color)
            lay.addWidget(l_color)
            button.setLayout(lay)

        layout_group.addLayout(grid_layout_settings)

        # Add action buttons
        lhb_buttun = QHBoxLayout()
        self.btn_validate = QPushButton("Confirm")
        lhb_buttun.addWidget(self.btn_validate)
        self.btn_cancel = QPushButton("Cancel")
        lhb_buttun.addWidget(self.btn_cancel)
        layout_group.addLayout(lhb_buttun)

        group_box.setLayout(layout_group)
        parent.setLayout(layout)


class ViewShowChannels(QDialog):
    def __init__(self, data:DataContainer):
        super().__init__()

        self.data = data
        self._changed = False

        self.ui = ViewShowChannelsUI(self, data)
        for i, (button, label) in enumerate(zip(self.ui.buttons, self.ui.l_colors)):
            button.clicked.connect(self._on_btn_color_select_clicked)
            label.setStyleSheet(f"background-color: {self.data.y[i].color.hex};")
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

    def _on_btn_color_select_clicked(self):
        index = self.ui.buttons.index(self.sender())
        dialog = QColorDialog()
        dialog.setCurrentColor(QColor(*self.data.y[index].color.rgb_int))
        dialog.exec()
        color = dialog.selectedColor()
        if color.isValid():
            color = colors.from_rgba_int(color.toTuple())
            self.data.y[index].set(color=color)
            self.ui.l_colors[index].setStyleSheet(f"background-color: {color.hex}")

    # Methods

    def has_changed(self):
        return self._changed
