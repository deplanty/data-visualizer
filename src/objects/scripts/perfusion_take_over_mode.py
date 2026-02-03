import copy

import matplotlib.pyplot as plt
import numpy as np

from src.objects.scripts_loader import BaseScript


def get_between(
    x: np.ndarray, y: np.ndarray, start: float, end: float
) -> tuple[np.ndarray, np.ndarray]:
    """
    Return the x and y regions where `start < x < end`.

    :param x: The x data.
    :type x: np.ndarray
    :param y: The y data.
    :type y: np.ndarray
    :param start: The starting point where the data should be cropped.
    :type start: float
    :param end: The ending point where the data should be cropped.
    :type end: float
    :return: The x and y cropped regions.
    :rtype: tuple[ndarray[Any, Any], ndarray[Any, Any]]
    """

    to_end = x < end
    from_start = x > start
    keep = from_start * to_end

    return x[keep], y[keep]


def remove_spikes(curve: np.ndarray, window: int = 50, height_factor: float = 1.5) -> np.ndarray:
    """
    Remove the spikes from a curve.

    :param curve: The data containing spikes.
    :type curve: np.ndarray
    :param window: The number of elements to use to determine if a peak is a spike.
    :type window: int
    :return: The curve without the spikes.
    :rtype: ndarray[Any, Any]
    """

    curve_cut = copy.deepcopy(curve)
    n_segments: int = len(curve) // window
    for i in range(n_segments):
        segment = curve[i * window : (i + 1) * window]
        median = np.median(segment)
        for j in range(window):
            if segment[j] < median / height_factor or segment[j] > median * height_factor:
                curve_cut[i * window + j] = median

    return curve_cut


def analyze_tom(data, cursor, detection: float, duration_mean: float = 60):
    """
    Analyze the Take Over Mode of the given region.

    :param data:
    :type data: DataContainer
    :param cursor:
    :type cursor: Cursor
    :param detection: The factor of `max - min` to detect the TOM.
    :type detection: float
    :param duration_mean: The duration (in seconds) to compute the flow mean.
    :type duration_mean: float
    """

    x = np.array(data.x.values)
    y = np.array(data.y[0].values)
    start = cursor.start
    end = cursor.end

    # Compute the mean before the take over
    _, first_y = get_between(x, y, start - duration_mean, start)
    mean_first = np.mean(first_y)

    # Compute the mean after the take over
    _, last_y = get_between(x, y, end, end + duration_mean)
    mean_last = np.mean(last_y)

    # Remove the spikes in the selected region
    x, y_unspiked = get_between(x, y, start, end)
    y_unspiked = remove_spikes(y_unspiked, window=100, height_factor=1.2)

    # Determine the threshold to detect the start and end of TOM
    delta = np.max([mean_first, mean_last]) - np.min(y_unspiked)
    y_detection = delta * detection

    # Get the duration of the take over mode
    tom_start = 0
    tom_start_index = 0
    tom_end = 0
    tom_end_index = 0
    # Find start of TOM
    for i in range(0, len(x)):
        if y_unspiked[i] < y_detection:
            tom_start = x[i]
            tom_start_index = i
            break
    # Find end of TOM
    for i in range(tom_start_index, len(x)):
        if y_unspiked[i] > y_detection:
            tom_end = x[i]
            tom_end_index = i
            break

    # Mean value during the TOM
    mean_tom = np.mean(y[tom_start_index:tom_end_index])

    print(f"Detection: {detection * 100:2.1f}%")
    print(f"Mean before TOM: {mean_first:.2f}")
    print(f"Mean after TOM: {mean_last:.2f}")
    print(f"Mean TOM: {mean_tom:.2f}")
    print(f"Duration: {tom_end - tom_start:.1f} s")
    print("")


class PerfusionTakeOverModeScript(BaseScript):
    name = "Perfusion evaluation of the Take Over Mode"
    description = "Evaluate the Take Over Mode"

    @staticmethod
    def process(data, cursor):
        analyze_tom(data, cursor, 0.5, 60)
        analyze_tom(data, cursor, 0.1, 60)
