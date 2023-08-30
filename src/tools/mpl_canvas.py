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

        self.axes = list()
        self.spans = list()

    # Events

    def _on_selection_changed(self, xmin, xmax):
        self.signal_selection_changed.emit(xmin, xmax)

    # Method

    def draw_data(self, data:DataContainer):
        self.fig.clear()
        rows = data.size(only_show=True)
        if rows == 0:
            self.fig.canvas.draw()
            return
        elif rows == 1:
            self.axes = [self.fig.subplots(data.size(only_show=True), 1, sharex=True)]
        else:
            self.axes = self.fig.subplots(data.size(only_show=True), 1, sharex=True)

        i = 0
        for j, y in enumerate(data.y):
            # Continue if the axis should not be shown
            if not y.show:
                continue
            ax = self.axes[i]
            ax.plot(data.get_x_data(), data.get_y_data(j))
            ax.set_ylabel(data.y[j].label)
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

        self.axes[-1].set_xlabel(data.x.label)
        self.fig.subplots_adjust(hspace=0)
        self.fig.canvas.draw()

    def get_selection(self) -> list:
        return self.spans[0].extents
