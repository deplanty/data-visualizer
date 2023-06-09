# import asl5000_utils as asl

from PySide6.QtCore import Signal

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector


class MplCanvas(FigureCanvasQTAgg):
    signal_selection_changed = Signal(float, float)

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)

        self.data = [[1, 2, 3, 4], [8, 10, 6, 5], [0, 1, 0, 2]]  # x, y1, y2
        self.axes = list()
        self.spans = list()

    # Events

    def _on_selection_changed(self, xmin, xmax):
        self.signal_selection_changed.emit(xmin, xmax)

    # Method

    def load_file(self, filename:str):
        """
        Loads a file and plots it.

        Args:
            filename (str): path to file.
        """

        self.data = [[1, 2, 3, 4], [8, 10, 6, 5], [0, 1, 0, 2]]  # x, y1, y2
        self.draw_data()
        self.fig.canvas.draw()

    def draw_data(self):
        rows = len(self.data)
        self.axes.clear()
        for i in range(1, rows):
            ax = self.fig.add_subplot(rows - 1, 1, i)
            ax.plot(self.data[0], self.data[i])
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
            self.axes.append(ax)
            self.spans.append(span)

    def get_n_channels(self) -> int:
        return len(self.data) - 1

    def get_selection(self) -> list:
        return self.spans[0].extents
