import copy
from typing import TYPE_CHECKING

import numpy as np
from scipy.signal import savgol_filter

from src.objects.scripts_loader import BaseScript
from src.objects import Series
from src.windows import DialogMultiInput
from src import logger

if TYPE_CHECKING:
    from src.objects import Acquisition, SeriesCollection, GraphCursor


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

    keep = (start < x) & (x < end)
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

    return curve_cut  # type: ignore


def remove_spikes_bis(
    curve: np.ndarray, window: int = 50, height_factor: float = 1.5
) -> np.ndarray:
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
    win_half = window // 2
    for i in range(win_half, len(curve) - win_half):
        segment = curve[i - win_half : i + win_half]
        median = np.median(segment)
        if curve[i] < median / height_factor or curve[i] > median * height_factor:
            curve_cut[i] = median

    curve_cut = savgol_filter(curve_cut, window, 2)

    return curve_cut  # type: ignore


def analyze_tom(
    data: "SeriesCollection",
    cursor: "GraphCursor",
    detection: float,
    duration_mean: float = 60,
    tom_min_duration: float = 5,
    display_smoothed: bool = False,
):
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
    :param tom_min_duration: The minimum duration of the TOM.
    :type tom_min_duration: float
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
    x_selected, y_selected = get_between(x, y, start, end)
    y_unspiked = remove_spikes_bis(y_selected, window=50, height_factor=1.25)

    # Add a series to display the curved with the spikes removed
    if display_smoothed:
        series = Series()
        series.set_values(remove_spikes_bis(y, window=50, height_factor=1.25))  # type: ignore
        series.set(title="Smooth", unit=data.y[0].unit)
        data.add_series(series)

    # Determine the threshold to detect the start and end of TOM
    delta = np.max([mean_first, mean_last]) - np.min(y_unspiked)
    y_detection = delta * detection

    # Get the duration of the take over mode
    tom_start = 0
    tom_start_index = 0
    tom_end = 0
    tom_end_index = 0
    # Find start of TOM
    for i in range(0, len(x_selected)):
        if y_unspiked[i] < y_detection:
            tom_start = x_selected[i]
            tom_start_index = i
            break
    # Find end of TOM
    for i in range(tom_start_index, len(x_selected)):
        if y_unspiked[i] > y_detection:
            tom_end = x_selected[i]
            tom_end_index = i
            if tom_end - tom_start > tom_min_duration:
                break

    cursor.set_and_emit(tom_start, tom_end)

    # Mean value during the TOM
    mean_tom = np.mean(y_selected[tom_start_index:tom_end_index])

    y_unit = data.y[0].unit
    logger.journal("Results:")
    logger.journal(f" - Mean before TOM: {mean_first:.2f} {y_unit}")
    logger.journal(f" - Mean after TOM: {mean_last:.2f} {y_unit}")
    logger.journal(f" - Mean TOM: {mean_tom:.2f} {y_unit}")
    logger.journal(f" - Duration: {tom_end - tom_start:.1f} s")
    logger.journal("")


class PerfusionTakeOverModeScript(BaseScript):
    name = "Perfusion evaluation of the Take Over Mode..."
    description = "Evaluate the Take Over Mode"

    @classmethod
    def _process(cls, acquisition: "Acquisition", cursor: "GraphCursor"):
        dialog = DialogMultiInput()
        dialog.add_input_float("Percent of Peak-Peak", "%", 50)
        dialog.add_input_float("Duration to compute mean", "s", 60)
        dialog.add_input_float("TOM mean duration", "s", 5)
        dialog.add_input_bool("Display smoothed curve", False)
        dialog.exec()

        if not dialog.confirmed:
            return

        values = dialog.get_values()
        detection = values["Percent of Peak-Peak"] / 100
        duration_mean = values["Duration to compute mean"]
        tom_mean_duration = values["TOM mean duration"]
        display_smoothed = values["Display smoothed curve"]

        logger.journal(f" - Filename: {acquisition.filename}")
        logger.journal(f"- Time start: {cursor.start:.2f}")
        logger.journal(f"- Time end: {cursor.end:.2f}")
        for key, value in dialog.get_values().items():
            logger.journal(f" - {key}: {value}")

        analyze_tom(
            acquisition.series,
            cursor,
            detection,
            duration_mean,
            tom_mean_duration,
            display_smoothed,
        )
