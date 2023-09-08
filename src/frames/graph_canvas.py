import pyqtgraph as pg

from src.objects import DataContainer, colors


pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


class GraphCanvas(pg.GraphicsLayoutWidget):
    def __init__(self):
        super().__init__()
        self.axes = list()
        self.spans = list()

    def draw_data(self, data:DataContainer):

        rows = data.size(only_show=True)
        # Draw the channels
        for i, channel in enumerate(data.y):
            # Continue if the axis should not be shown
            if not channel.show:
                continue

            plt = self.addPlot(row=i, col=0)
            plt.plot(data.x.values, channel.values)
            self.axes.append(plt)

            lr = pg.LinearRegionItem()
            plt.addItem(lr)
            self.spans.append(lr)

            # if channel.color is None:
            #     channel.color = next(self.ch_colors)
            # ax.plot(
            #     data.get_x_data(),
            #     channel.values,
            #     color=channel.color.rgb,
            #     linewidth=0.75,
            # )
            # ax.set_ylabel(channel.label)
            # ax.grid(which="major", linestyle="dashed", linewidth=0.5)
            # span = SpanSelector(
            #     ax=ax,
            #     minspan=-1,
            #     onselect=self._on_selection_changed,
            #     direction="horizontal",
            #     useblit=True,
            #     props=dict(facecolor="black", alpha=0.05),
            #     interactive=True,
            #     drag_from_anywhere=True,
            #     onmove_callback=self._on_selection_changed
            # )
            # self.spans.append(span)

        # self.axes[-1].set_xlabel(data.x.label)
        # self.fig.subplots_adjust(hspace=0)
        # self.fig.canvas.draw()
