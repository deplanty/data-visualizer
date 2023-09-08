import numpy as np
from PySide6 import QtWidgets

from src.objects import Cursor, DataLoader, DataContainer, DataAnalyzer, ScriptsLoader
from src.windows import ViewShowChannels

from .mainwindow_ui import MainWindowUI


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.data = DataContainer()
        self.cursor = Cursor()
        self.cursor.changed.connect(self._on_cursor_changed)

        self.ui = MainWindowUI(self)
        self.ui.menu_file_open.triggered.connect(self._on_menu_file_open_triggered)
        self.ui.menu_file_exit.triggered.connect(self._on_menu_file_exit_triggered)
        self.ui.menu_view_show_channels.triggered.connect(self._on_menu_view_show_channels_triggered)
        for name in ScriptsLoader.list_all():
            menu = self.ui.add_script_menu(name)
            menu.triggered.connect(self._on_menu_scripts_triggered)
        self.ui.mpl_canvas.signal_selection_changed.connect(self._on_selection_changed)
        for row in self.ui.grid:
            row["measure"].activated.connect(self.on_combobox_changed)
            row["channel"].activated.connect(self.on_combobox_changed)

        self.load_from_file("test/rigel_multiflo.csv", "CSV from Rigel Multiflo (*.csv)")

    # Events

    def _on_menu_file_exit_triggered(self):
        self.close()

    def _on_menu_file_open_triggered(self):
        valid_files = ";;".join([
            *DataLoader.list_all_file_type(),
            "All Files (*.*)",
        ])
        filename, file_type = QtWidgets.QFileDialog.getOpenFileName(self, "Open a file", "", valid_files)
        if not filename:
            return

        self.load_from_file(filename, file_type)

    def _on_menu_view_show_channels_triggered(self):
        dialog = ViewShowChannels(self.data)
        dialog.exec()
        if dialog.has_changed():
            # Redraw to show only selected channels
            self.ui.mpl_canvas.draw_data(self.data)

    def _on_menu_scripts_triggered(self):
        action = self.sender()
        ScriptsLoader.process(action.text(), self.data, self.cursor)

    def _on_selection_changed(self, xmin:float, xmax:float):
        """
        When the selection is changed.

        Args:
            xmin (float): miniumum x value.
            xmax (float): maximum x value.
        """
        # Check if the selection is set or not

        for span in self.ui.mpl_canvas.spans:
            span.extents = (xmin, xmax)
            span.set_visible(True)

        self.cursor.set(xmin, xmax)
        self.process_measures(xmin, xmax)

    def _on_cursor_changed(self, xmin, xmax):
        for span in self.ui.mpl_canvas.spans:
            span.extents = (xmin, xmax)
            span.set_visible(True)

    def on_combobox_changed(self):
        xmin, xmax = self.ui.mpl_canvas.get_selection()
        self.process_measures(xmin, xmax)

    # Methods

    def load_from_file(self, filename:str, file_type:str):
        self.data = DataLoader.load(filename, file_type)
        self.ui.mpl_canvas.draw_data(self.data)
        self.ui.set_channels(len(self.data))

    def process_measures(self, xmin:float, xmax:float):
        # Process the selection
        x = self.data.get_x_data()

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
            region_y = self.data.get_y_data(channel, (i_min, i_max))

            value = DataAnalyzer.process(measure, region_x, region_y)
            row["label"].setText(f"{value:0.5f}")
