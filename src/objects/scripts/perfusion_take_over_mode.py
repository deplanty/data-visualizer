import numpy as np

from src.objects.scripts_loader import BaseScript


def get_between(x: np.ndarray, y: np.ndarray, start: float, end: float):
    to_end = x < end
    from_start = x > start
    keep = from_start * to_end

    return x[keep], y[keep]


class PerfusionTakeOverModeScript(BaseScript):
    name = "Perfusion evaluation of the Take Over Mode"
    description = "Evaluate the Take Over Mode"

    @staticmethod
    def process(data, cursor):
        x = np.array(data.x.values)
        y = np.array(data.y[0].values)
        start = cursor.start
        end = cursor.end

        duration_mean = 60  # sec

        # Compute the mean before the take over
        cursor.set_and_emit(start - duration_mean, start)
        _, first_y = get_between(x, y, start - duration_mean, start)
        mean_first = np.mean(first_y)

        # Compute the mean after the take over
        cursor.set_and_emit(end, end + duration_mean)
        _, last_y = get_between(x, y, end, end + duration_mean)
        mean_last = np.mean(last_y)

        # Get the duration of the take over mode
        y_start_50 = mean_first * 0.5
        y_end_50 = mean_last * 0.5

        tom_start = 0
        tom_start_index = 0
        tom_end = 0
        tom_end_index = 0
        index = np.searchsorted(x, start)
        window_half = 20
        # Find start of TOM
        for i in range(index, len(x)):
            if np.mean(y[i - window_half : i + window_half]) < y_start_50:
                tom_start = x[i]
                tom_start_index = i
                break
        # Find end of TOM
        for i in range(tom_start_index, len(x)):
            if np.mean(y[i - window_half : i + window_half]) > y_end_50:
                tom_end = x[i]
                tom_end_index = i
                break
        cursor.set_and_emit(tom_start, tom_end)
