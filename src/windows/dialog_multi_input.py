from typing import Any

from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QDoubleSpinBox,
    QCheckBox,
)


class DialogMultiInputUi:
    def __init__(self, widget: QDialog):
        vlayout = QVBoxLayout()
        widget.setLayout(vlayout)

        self.glayout = QGridLayout()
        vlayout.addLayout(self.glayout)

        hlayout = QHBoxLayout()
        vlayout.addLayout(hlayout)
        self.button_confirm = QPushButton()
        self.button_confirm.setText("Confirm")
        hlayout.addWidget(self.button_confirm)
        self.button_cancel = QPushButton()
        self.button_cancel.setText("Cancel")
        hlayout.addWidget(self.button_cancel)

        self._row = 0
        self.items = dict()

    def add_input_float(self, text: str, suffix: str = "", default: float = 0):
        label = QLabel()
        label.setText(text)
        self.glayout.addWidget(label, self._row, 0)
        value = QDoubleSpinBox()
        value.setMinimum(-float("inf"))
        value.setMaximum(float("inf"))
        value.setValue(default)
        value.setSuffix(suffix)
        self.glayout.addWidget(value, self._row, 1)

        self._row += 1
        self.items[text] = value

    def add_input_bool(self, text: str, default: bool = False):
        check = QCheckBox()
        check.setText(text)
        check.setChecked(default)
        self.glayout.addWidget(check, self._row, 0, 1, 2)

        self._row += 1
        self.items[text] = check


class DialogMultiInput(QDialog):
    def __init__(self):
        super().__init__()

        self.ui = DialogMultiInputUi(self)
        self.ui.button_confirm.clicked.connect(self._on_button_confirm_clicked)
        self.ui.button_cancel.clicked.connect(self._on_button_cancel_clicked)

        self.confirmed = False

    # Events

    def _on_button_confirm_clicked(self):
        self.confirmed = True
        self.accept()

    def _on_button_cancel_clicked(self):
        self.confirmed = False
        self.reject()

    # Methods

    def add_input_float(self, text: str, suffix: str = "", default: float = 0):
        self.ui.add_input_float(text, suffix, default)

    def add_input_bool(self, text: str, default: bool = False):
        self.ui.add_input_bool(text, default)

    def get_values(self) -> dict[str, Any]:
        values = dict()

        for key, widget in self.ui.items.items():
            if hasattr(widget, "value"):
                values[key] = widget.value()
            elif hasattr(widget, "isChecked"):
                values[key] = widget.isChecked()
            else:
                raise NotImplementedError("Widget {widget} not implemented yet")

        return values
