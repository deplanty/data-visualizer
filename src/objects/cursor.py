from PySide6.QtCore import Signal, QObject


class Cursor(QObject):
    changed = Signal(float, float)

    def __init__(self):
        super().__init__()

        self._start = 0.0
        self._end = 0.0

    def __str__(self):
        return f"Cursor({round(self.start, 3)}, {round(self.end, 3)})"

    @property
    def start(self) -> float:
        return self._start

    @property
    def end(self) -> float:
        return self._end

    def set(self, start:float, end:float):
        if start <= end:
            self._start = start
            self._end = end
        else:
            self._start = end
            self._end = start

    def get(self) -> tuple:
        return self.start, self.end

    def set_and_emit(self, start:float, end:float):
        self.set(start, end)
        self.changed.emit(start, end)
