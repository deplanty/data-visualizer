
class DataColumn:
    _values: list[float]
    title: str
    unit: str
    show: bool

    def __init__(self):
        self._values = list()
        self.title = str()
        self.unit = str()
        self.show = True

    def __str__(self):
        n = len(self._values)
        # Process label
        if self.label == "":
            label = ""
        else:
            label = self.label + ": "
        # Process quantity
        if n == 0:
            return f"{label}Empty"
        elif n == 1:
            return f"{label}{n} value"
        else:
            return f"{label}{n} values"

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

    def set(self, values:list=None, title:str=None, unit:str=None, show:bool=None):
        """
        Set the values for the parameters.

        Args:
            values (list): clear current values and replace with new. If None, do nothing.
            title (str): the new title. If None, do nothing.
            unit (str): the new unit. If None, do nothing.
        """

        if values is not None:
            self._values.clear()
            self._values.extend(values)

        if title is not None:
            self.title = title

        if unit is not None:
            self.unit = unit

        if show is not None:
            self.show = show


class DataContainer:
    def __init__(self):
        self._x = DataColumn()
        self._y = list()

    def __len__(self):
        return len(self._y)

    # Properties

    @property
    def x(self) -> DataColumn:
        return self._x

    @property
    def y(self):
        return self._y

    # Getter setter

    def get_x_data(self) -> list:
        return self._x.values

    def get_y_data(self, index:int, slice_:tuple=None) -> list:
        if slice_ is None:
            return self._y[index].values
        else:
            return self._y[index].values[slice(*slice_)]

    # Methods

    def init(self, size:int):
        self._x.init()
        self._y = [DataColumn() for _ in range(size)]

    def add_row(self, values:list[float], x_index:int=0):
        self._x.values.append(float(values.pop(x_index)))

        if len(values) < len(self._y):
            raise ValueError("Not enough data to add in container.")
        if len(values) > len(self._y):
            raise ValueError("Attemping to add too many data in container.")

        for i, value in enumerate(values):
            self._y[i].values.append(float(value))

    def size(self, only_show=False):
        if only_show:
            return sum([1 for y in self._y if y.show])
        else:
            return len(self._y)



if __name__ == '__main__':
    data = DataContainer()
    data.init(4)
    data.add_row([1, 2, 3, 4, 5])
    data.x.title = "Time"
    data.x.unit = "sec"
    print(data.x)
    print(data.y[0])
    print(data.y[1])


