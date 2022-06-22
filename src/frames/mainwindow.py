import numpy as np
from PyQt5 import QtWidgets

from .mainwindow_ui import MainWindowUI


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = MainWindowUI(self)

        self.ui.menu_file_open.triggered.connect(self._on_menu_file_open_triggered)
        self.ui.menu_file_exit.triggered.connect(self._on_menu_file_exit_triggered)
        self.ui.mpl_canvas.signal_selection_changed.connect(self._on_selection_changed)
        for row in self.ui.grid:
            row["measure"].activated.connect(self.on_combobox_changed)
            row["channel"].activated.connect(self.on_combobox_changed)

    # Events

    def _on_menu_file_exit_triggered(self):
        self.close()

    def _on_menu_file_open_triggered(self):
        result = QtWidgets.QFileDialog.getOpenFileName(self, "Open a file", "", "All Files (*.*)")
        filename = result[0]
        if not filename:
            return

        self.ui.mpl_canvas.load_file(filename)
        self.ui.set_channels(self.ui.mpl_canvas.get_n_channels())

    def _on_selection_changed(self, xmin:float, xmax:float):
        """
        When the selection is changed.

        Args:
            xmin (float): miniumum x value.
            xmax (float): maximum x value.
        """
        # Check if the selection is set of not
        if xmin == xmax:
            for span in self.ui.mpl_canvas.spans:
                span.extents = (0, 0)
                span.set_visible(False)
        else:
            for span in self.ui.mpl_canvas.spans:
                span.extents = (xmin, xmax)
                span.set_visible(True)
                self.process_measures(xmin, xmax)

    def on_combobox_changed(self):
        xmin, xmax = self.ui.mpl_canvas.get_selection()
        self.process_measures(xmin, xmax)

    # Methods

    def process_measures(self, xmin:float, xmax:float):
        # Process the selection
        data = self.ui.mpl_canvas.data
        x = data[0]

        i_min, i_max = np.searchsorted(x, (xmin, xmax))
        i_max = min(len(x) - 1, i_max)
        if i_min == i_max:
            return
        # region_x = x[i_min:i_max]

        for row in self.ui.grid:
            measure = row["measure"].currentText()
            channel = int(row["channel"].currentText())
            region_y = data[channel][i_min:i_max]
            value = 0.0
            if measure == "Minimum":
                value = np.min(region_y)
            elif measure == "Maximum":
                value = np.max(region_y)
            elif measure == "Mean":
                value = np.mean(region_y)
            row["label"].setText(f"{value:0.5f}")
