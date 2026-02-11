import os

from PySide6.QtWidgets import (
    QWidget,
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
)
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon

from src.objects import DataLoader
import src.preload as pl


class WidgetOpenAcquisition(QWidget):
    file_selected = Signal(str, str)

    def __init__(self):
        super().__init__()

        self._file_types: list[str] = list()
        self._file_type_selected = str()
        self._filename_selected = str()

        # A very simple UI
        hlayout = QHBoxLayout()
        self.setLayout(hlayout)

        self._label = QLabel()
        self._label.setText("...")
        hlayout.addWidget(self._label, stretch=1)
        button_open = QPushButton()
        button_open.setIcon(QIcon(":/icons/open-file"))
        hlayout.addWidget(button_open)

        # Connect signals
        button_open.clicked.connect(self._on_button_open_clicked)

    # Properties

    @property
    def filename_selected(self) -> str:
        return self._filename_selected

    # Events

    def _on_button_open_clicked(self):
        valid_files = ";;".join(self._file_types)
        filename, file_type = QFileDialog.getOpenFileName(
            self, "Open a file", "", valid_files, self._file_type_selected
        )

        if not filename:
            return

        # Shorten the filename to limit the size of the window and show the full path as a tooltip
        self._label.setText(os.path.basename(filename))
        self._label.setToolTip(filename)
        self._filename_selected = filename
        self.file_selected.emit(filename, file_type)

    # Methods

    def set_file_types(self, file_types: list[str], selected: str = ""):
        self._file_types = file_types
        self._file_type_selected = selected


class DialogOpenAcquisitionUi:
    def __init__(self, widget: QDialog):
        vlayout = QVBoxLayout()
        widget.setLayout(vlayout)

        flayout = QFormLayout()
        vlayout.addLayout(flayout)

        self.ask_open = WidgetOpenAcquisition()
        flayout.addRow("File:", self.ask_open)
        self.loader = QComboBox()
        flayout.addRow("Loader:", self.loader)

        hlayout = QHBoxLayout()
        vlayout.addLayout(hlayout)
        self.button_confirm = QPushButton()
        self.button_confirm.setText("Confirm")
        hlayout.addWidget(self.button_confirm)
        self.button_cancel = QPushButton()
        self.button_cancel.setText("Cancel")
        hlayout.addWidget(self.button_cancel)


class DialogOpenAcquisition(QDialog):
    def __init__(self):
        super().__init__()

        self.ui = DialogOpenAcquisitionUi(self)
        self.ui.ask_open.file_selected.connect(self._on_ask_open_file_selected)
        self.ui.button_confirm.clicked.connect(self._on_button_confirm_clicked)
        self.ui.button_cancel.clicked.connect(self._on_button_cancel_clicked)

        self.ui.ask_open.set_file_types(
            ["All Files (*.*)", *DataLoader.list_all_file_type()],
            pl.settings.get("last_open_file_type"),
        )
        self.ui.loader.addItems(DataLoader.list_all_file_type())
        self.ui.loader.setCurrentText(pl.settings.get("last_open_file_type"))

        self.confirmed = False

    # Events

    def _on_ask_open_file_selected(self, filename: str, file_type: str):
        self.ui.loader.setCurrentText(file_type)
        pl.settings.set("last_open_file_type", file_type)

    def _on_button_confirm_clicked(self):
        if self.ui.ask_open.filename_selected:
            self.confirmed = True
            self.accept()
        else:
            self.confirmed = False
            self.reject()

    def _on_button_cancel_clicked(self):
        self.confirmed = False
        self.reject()

    # Methods

    def get_values(self) -> tuple[str, str]:
        """
        :return: The filename and file type selected by the user
        :rtype: tuple(str, str)
        """

        return self.ui.ask_open.filename_selected, self.ui.loader.currentText()
