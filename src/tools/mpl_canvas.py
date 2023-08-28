# import asl5000_utils as asl
import re

from PySide6.QtCore import Signal

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector

from src.objects import DataContainer


class MplCanvas(FigureCanvasQTAgg):
    signal_selection_changed = Signal(float, float)

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)

        self.toolbar = NavigationToolbar2QT(self)

        self.data = DataContainer()
        self.axes = list()
        self.spans = list()

    # Events

    def _on_selection_changed(self, xmin, xmax):
        self.signal_selection_changed.emit(xmin, xmax)

    # Method

    def load_file(self, filename:str, selector):
        """
        Loads a file and plots it.

        Args:
            filename (str): path to file.
        """

        can_draw = False

        if selector == "CSV from Rigel Multoflo (*.csv)":
            with open(filename, "r") as fid:
                # 1 (x) + 4 (y) columns of data
                self.data.init(size=4)

                # 14 lines of useless header
                for _ in range(14): fid.readline()
                # Add metadata
                self.data.x.title = "Temps"
                self.data.x.unit = "sec"
                self.data.y[0].title = "Volume cumulé"
                self.data.y[0].unit = "ml"
                self.data.y[0].show = True
                self.data.y[1].title = "Débit instantané"
                self.data.y[1].unit = "ml/h"
                self.data.y[1].show = True
                self.data.y[2].title = "Debit moyen"
                self.data.y[2].unit = "ml/h"
                self.data.y[2].show = False
                self.data.y[3].title = "Pression"
                self.data.y[3].unit = "mmHg"
                self.data.y[3].show = False

                for line in fid:
                    line = line.rstrip().split(",")
                    # End when empty table line
                    if line[0] == "":
                        break
                    # Add the 5 columns in data
                    self.data.add_row(line[:5], x_index=0)

                can_draw = True

        if can_draw:
            self.draw_data()
            self.fig.canvas.draw()

    def draw_data(self):
        self.fig.clear()
        self.axes = self.fig.subplots(self.data.size(only_show=True), 1, sharex=True)

        i = 0
        for j, y in enumerate(self.data.y):
            # Continue if the axis should not be shown
            if not y.show:
                continue
            ax = self.axes[i]
            ax.plot(self.data.get_x_data(), self.data.get_y_data(j))
            ax.set_ylabel(self.data.y[j].label)
            ax.grid(linestyle="dashed")
            span = SpanSelector(
                ax=ax,
                onselect=self._on_selection_changed,
                direction="horizontal",
                useblit=True,
                props={"alpha": 0.2, "facecolor":"grey"},
                interactive=True,
                drag_from_anywhere=True,
                onmove_callback=self._on_selection_changed
            )
            self.spans.append(span)
            i += 1

        self.fig.subplots_adjust(hspace=0)
        self.axes[-1].set_xlabel(self.data.x.label)

    def get_n_channels(self) -> int:
        return len(self.data)

    def get_selection(self) -> list:
        return self.spans[0].extents
