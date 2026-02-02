from src.objects.data_analyzer import BaseAnalyzer

import numpy as np


class NoneAnalyzer(BaseAnalyzer):
    name = "None"
    description = "Does nothing."

    @staticmethod
    def process(region_x: list, region_y: list):
        return 0


class ValueAnalyzer(BaseAnalyzer):
    name = "Value"
    description = "Get the last value of the region."

    @staticmethod
    def process(region_x: list, region_y: list) -> float:
        return region_y[-1]


class MinimumAnalyzer(BaseAnalyzer):
    name = "Minimum"
    description = "Get the minimum value in the region."

    @staticmethod
    def process(region_x: list, region_y: list) -> float:
        import numpy as np

        return np.min(region_y)


class MaximumAnalyzer(BaseAnalyzer):
    name = "Maximum"
    description = "Get the maximum value in the region."

    @staticmethod
    def process(region_x: list, region_y: list) -> float:
        import numpy as np

        return np.max(region_y)


class MeanAnalyzer(BaseAnalyzer):
    name = "Mean"
    description = "Compute the mean value in the region"

    @staticmethod
    def process(region_x: list, region_y: list) -> float:
        import numpy as np

        return np.mean(region_y)  # type: ignore


class DetaTAnalyzer(BaseAnalyzer):
    name = "Delta T"
    description = "Get the region duration."

    @staticmethod
    def process(region_x: list, region_y: list) -> float:
        import numpy as np

        if len(region_x) > 1:
            return np.max(region_x) - np.min(region_x)
        else:
            return 0


class PeakPeakAnalyzer(BaseAnalyzer):
    name = "Peak-Peak"
    description = "Compute the difference between the maximum and minimum value in the region."

    @staticmethod
    def process(region_x: list, region_y: list) -> float:
        import numpy as np

        if len(region_x) > 1:
            return np.max(region_y) - np.min(region_y)
        else:
            return 0


class IntegrateAnalyzer(BaseAnalyzer):
    name = "Integrate"
    description = "Compute the area under the curve of the region."

    @staticmethod
    def process(region_x: list, region_y: list) -> float:
        import numpy as np

        return np.trapezoid(region_y, x=region_x)
