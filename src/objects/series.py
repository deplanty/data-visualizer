import numpy as np
from PySide6.QtCore import QObject, Signal

from src.objects import colors


class Series:
    _values: list[float]
    title: str
    unit: str
    visible: bool
    color: colors.Color

    def __init__(self):
        self._values = list()
        self.title = str()
        self.unit = str()
        self.visible = True
        self.color = next(colors.sample)

    def __str__(self):
        # Process label
        if self.label == "":
            label = ""
        else:
            label = self.label + ": "

        # Process quantity
        n = len(self._values)
        if n == 0:
            quantity = "Empty"
        elif n == 1:
            quantity = f"{n} value"
        else:
            quantity = f"{n} values"

        return f"{label}{quantity}"

    def __len__(self):
        return len(self._values)

    # Properties

    @property
    def values(self):
        return self._values

    @property
    def label(self):
        if self.title and self.unit:
            label = f"{self.title} ({self.unit})"
        elif self.title and not self.unit:
            label = f"{self.title}"
        elif not self.title and self.unit:
            label = f"({self.unit})"
        else:
            label = ""

        return label

    # Methods

    def init(self):
        self._values.clear()
        self.title = ""
        self.unit = ""

    def set_values(self, values: list):
        self._values.clear()
        self._values.extend(values)

    def set_title(self, title: str):
        self.title = title

    def set_unit(self, unit: str):
        self.unit = unit

    def set_visible(self, enabled: bool):
        self.visible = enabled

    def set_color(self, color: tuple):
        self.color = colors.Color(color)

    def set(self, **kwargs):
        """
        Set the values for the parameters.

        :param values: Clear current values and replace with new.
        :type list:
        :param title: The new title.
        :type str:
        :param unit: The new unit.
        :type str:
        :param visible: The data is shown.
        :type bool:
        :param color: The color of the curve.
        :type tuple:
        """

        if "values" in kwargs:
            self.set_values(kwargs["values"])

        if "title" in kwargs:
            self.set_title(kwargs["title"])

        if "unit" in kwargs:
            self.set_unit(kwargs["unit"])

        if "visible" in kwargs:
            self.set_visible(kwargs["visible"])

        if "color" in kwargs:
            self.set_color(kwargs["color"])


class SeriesCollection(QObject):
    changed = Signal()

    def __init__(self):
        super().__init__()

        self._x = Series()
        self._y = list()

    def __len__(self):
        return len(self._y)

    # Properties

    @property
    def x(self) -> Series:
        return self._x

    @property
    def y(self):
        return self._y

    # Getter setter

    def get_x_data(self) -> list:
        return self._x.values

    def get_y_data(self, index: int, slice_: tuple | None = None) -> list:
        if slice_ is None:
            return self._y[index].values
        elif len(slice_) == 2 and slice_[0] == slice_[1]:
            if slice_[0] - 1 < 0:
                return [self._y[index].values[0]]
            else:
                return [self._y[index].values[slice_[0] - 1]]
        else:
            return self._y[index].values[slice(*slice_)]

    # Methods

    def init(self, channels: int):
        """
        Initialize the data with the number of channels it contains

        :param channels: The number of channels.
        :type channels: int
        """

        self._x.init()
        self._y = [Series() for _ in range(channels)]

    def add_row(self, values: list[float], x_index: int = 0):
        self._x.values.append(float(values.pop(x_index)))

        if len(values) < len(self._y):
            raise ValueError("Not enough data to add in container.")
        if len(values) > len(self._y):
            raise ValueError("Attemping to add too many data in container.")

        for i, value in enumerate(values):
            self._y[i].values.append(float(value))

    def size(self, only_show=False):
        if only_show:
            return sum([1 for y in self._y if y.visible])
        else:
            return len(self._y)

    def from_cursor(self, cursor):
        """
        Return a DataContainer with only the selected values
        """

        i_min, i_max = np.searchsorted(self.x.values, cursor.get())
        i_max = min(len(self.x) - 1, i_max)
        if i_min > i_max:
            i_min, i_max = i_max, i_min
        # Allow to take the last value
        if cursor.end > np.max(self.x.values):
            i_max += 1

        data = SeriesCollection()
        data.init(sum(1 for y in self.y if y.visible))

        data.x.set_values(self.x.values[i_min:i_max])
        data.x.set_title(title=self.x.title)
        data.x.set_unit(self.x.unit)
        data.x.set_color(self.x.color.rgb)

        for i, y in enumerate([y for y in self.y if y.visible]):
            data.y[i].set_values(y.values[i_min:i_max])
            data.y[i].set_title(y.title)
            data.y[i].set_unit(y.unit)
            data.y[i].set_color(y.color.rgb)

        return data

    def iter_rows(self):
        for i in range(len(self.x)):
            row = [self.x.values[i]]
            row.extend([y.values[i] for y in self.y])
            yield row

    def add_series(self, series: Series):
        self._y.append(series)
        self.changed.emit()
