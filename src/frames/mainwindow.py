import numpy as np
from PySide6 import QtWidgets

from .mainwindow_ui import MainWindowUI

from src.windows import ViewShowChannels


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = MainWindowUI(self)

        self.ui.menu_file_open.triggered.connect(self._on_menu_file_open_triggered)
        self.ui.menu_file_exit.triggered.connect(self._on_menu_file_exit_triggered)
        self.ui.menu_view_show_channels.triggered.connect(self._on_menu_view_show_channels)
        self.ui.mpl_canvas.signal_selection_changed.connect(self._on_selection_changed)
        for row in self.ui.grid:
            row["measure"].activated.connect(self.on_combobox_changed)
            row["channel"].activated.connect(self.on_combobox_changed)

    # Events

    def _on_menu_file_exit_triggered(self):
        self.close()

    def _on_menu_file_open_triggered(self):
        valid_files = ";;".join([
            "CSV from Rigel Multoflo (*.csv)",
            "All Files (*.*)",
        ])
        filename, selector = QtWidgets.QFileDialog.getOpenFileName(self, "Open a file", "", valid_files)
        if not filename:
            return

        self.ui.mpl_canvas.load_file(filename, selector)
        self.ui.set_channels(self.ui.mpl_canvas.get_n_channels())

    def _on_menu_view_show_channels(self):
        channels = list()
        for channel in self.ui.mpl_canvas.data.y:
            channels.append([channel.label, channel.show])

        self.w = ViewShowChannels(channels)
        self.w.exec()
        channels = self.w.get()
        if channels:
            # TODO: change graph to  show only selected channels
            ...


    def _on_selection_changed(self, xmin:float, xmax:float):
        """
        When the selection is changed.

        Args:
            xmin (float): miniumum x value.
            xmax (float): maximum x value.
        """
        # Check if the selection is set or not
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
        x = data.get_x_data()

        i_min, i_max = np.searchsorted(x, (xmin, xmax))
        i_max = min(len(x) - 1, i_max)
        if i_min == i_max:
            return
        if i_min > i_max:
            i_min, i_max = i_max, i_min

        # Allow to take the last value
        if xmax > np.max(x):
            i_max += 1

        region_x = x[i_min:i_max]
        for row in self.ui.grid:
            measure = row["measure"].currentText()
            channel = int(row["channel"].currentText()) - 1
            region_y = data.get_y_data(channel, (i_min, i_max))
            value = 0.0
            if measure == "Minimum":
                value = np.min(region_y)
            elif measure == "Maximum":
                value = np.max(region_y)
            elif measure == "Mean":
                value = np.mean(region_y)
            elif measure == "Delta T":
                value = np.max(region_x) - np.min(region_x)
            row["label"].setText(f"{value:0.5f}")
