# import asl5000_utils as asl
import re
import itertools

from PySide6.QtCore import Signal

import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector

from src.objects import DataContainer, colors

mpl.rc("lines", linewidth=0.5)


class MplCanvas(FigureCanvasQTAgg):
    signal_selection_changed = Signal(float, float)

    ch_colors = itertools.cycle([
        colors.RED,
        colors.GREEN,
        colors.BLUE,
        colors.YELLOW,
        colors.PURPLE,
        colors.CYAN,
    ])


    def __init__(self, width=5, height=4, dpi=100):
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
        # Manage subplot return value
        if rows == 0:
            self.fig.canvas.draw()
            return
        elif rows == 1:
            self.axes = [self.fig.subplots(data.size(only_show=True), 1, sharex=True)]
        else:
            self.axes = self.fig.subplots(data.size(only_show=True), 1, sharex=True)

        # Draw the channels
        i = 0
        for channel in data.y:
            # Continue if the axis should not be shown
            if not channel.show:
                continue
            ax = self.axes[i]
            if channel.color is None:
                channel.color = next(self.ch_colors)
            ax.plot(
                data.get_x_data(),
                channel.values,
                color=channel.color.rgb,
                linewidth=0.75,
            )
            ax.set_ylabel(channel.label)
            ax.grid(which="major", linestyle="dashed", linewidth=0.5)
            span = SpanSelector(
                ax=ax,
                minspan=-1,
                onselect=self._on_selection_changed,
                direction="horizontal",
                useblit=True,
                props=dict(facecolor="black", alpha=0.05),
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
