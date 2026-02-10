from typing import TYPE_CHECKING

import numpy as np
from PySide6.QtWidgets import QMainWindow, QFileDialog

from src.objects import (
    Acquisition,
    GraphCursor,
    DataLoader,
    SeriesCollection,
    DataAnalyzer,
    ScriptsLoader,
)
from src.windows import ViewShowChannels, DialogOpenAcquisition
import src.preload as pl
from src import logger

from .mainwindow_ui import MainWindowUI


if TYPE_CHECKING:
    from PySide6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.acquisition = Acquisition()
        self.graph_cursor = GraphCursor()
        self.graph_cursor.changed.connect(self._on_cursor_changed)

        self.ui = MainWindowUI(self)
        self.ui.menu_file_open.triggered.connect(self._on_menu_file_open_triggered)
        self.ui.menu_file_saveselectionas.triggered.connect(
            self._on_menu_file_saveselectionas_triggered
        )
        self.ui.menu_file_exit.triggered.connect(self._on_menu_file_exit_triggered)
        self.ui.menu_view_show_channels.triggered.connect(
            self._on_menu_view_show_channels_triggered
        )
        for name in ScriptsLoader.list_all():
            menu = self.ui.add_script_menu(name)
            menu.triggered.connect(self._on_menu_scripts_triggered)
        self.ui.figure_canvas.selection_changed.connect(self._on_selection_changed)
        for row in self.ui.grid:
            row["measure"].activated.connect(self._on_combobox_changed)
            row["channel"].activated.connect(self._on_combobox_changed)

        logger.set_journal(self.ui.journal)

    # Events

    def _on_menu_file_exit_triggered(self):
        self.close()

    def _on_menu_file_open_triggered(self):
        dialog = DialogOpenAcquisition()
        dialog.exec()
        if not dialog.confirmed:
            return

        filename, file_type = dialog.get_values()

        self.load_from_file(filename, file_type)

    def _on_menu_file_saveselectionas_triggered(self):
        filename = "test/export.csv"
        data = self.acquisition.series.from_cursor(self.graph_cursor)
        self.save_to_file(data, filename)

    def _on_menu_view_show_channels_triggered(self):
        dialog = ViewShowChannels(self.acquisition.series)
        dialog.exec()
        if dialog.has_changed():
            # Redraw to show only selected channels
            self.ui.figure_canvas.draw_data(self.acquisition.series)

    def _on_menu_scripts_triggered(self):
        action: "QAction" = self.sender()  # type: ignore
        ScriptsLoader.process(action.text(), self.acquisition, self.graph_cursor)

    def _on_selection_changed(self, xmin: float, xmax: float):
        """
        When the selection is changed.

        Args:
            xmin (float): miniumum x value.
            xmax (float): maximum x value.
        """
        # Check if the selection is set or not

        for span in self.ui.figure_canvas.spans:
            span.extents = (xmin, xmax)
            span.set_visible(True)

        self.graph_cursor.set(xmin, xmax)
        self.process_measures(xmin, xmax)

    def _on_cursor_changed(self, xmin, xmax):
        for span in self.ui.figure_canvas.spans:
            span.extents = (xmin, xmax)
            span.set_visible(True)

    def _on_combobox_changed(self):
        xmin, xmax = self.ui.figure_canvas.get_selection()
        self.process_measures(xmin, xmax)

    def _on_data_changed(self):
        self.update_ui_from_series()

    # Methods

    def load_from_file(self, filename: str, file_type: str):
        self.acquisition = DataLoader.load(filename, file_type)
        self.acquisition.series.changed.connect(self._on_data_changed)
        self.update_ui_from_series()

    def save_to_file(self, data: SeriesCollection, filename: str):
        with open(filename, "w") as fid:
            header = [data.x.label]
            header.extend([y.label for y in data.y])
            print(*header, sep=",", file=fid)
            for row in data.iter_rows():
                print(*row, sep=",", file=fid)

    def process_measures(self, xmin: float, xmax: float):
        # Process the selection
        series = self.acquisition.series
        x = series.get_x_data()

        i_min, i_max = np.searchsorted(x, (xmin, xmax))
        i_max = min(len(x) - 1, i_max)
        if i_min > i_max:
            i_min, i_max = i_max, i_min

        # Allow to take the last value
        if xmax > np.max(x):
            i_max += 1

        region_x = x[i_min:i_max]
        for row in self.ui.grid:
            measure = row["measure"].currentText()
            if measure == "None":
                continue

            channel = int(row["channel"].currentText()) - 1
            region_y = series.get_y_data(channel, (i_min, i_max))

            value = DataAnalyzer.process(measure, region_x, region_y)
            row["label"].setText(f"{value:0.5f}")

    def update_ui_from_series(self):
        self.ui.figure_canvas.draw_data(self.acquisition.series)
        self.ui.set_channels(len(self.acquisition.series))
