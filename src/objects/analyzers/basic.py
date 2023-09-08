class NoneAnalyzer(BaseAnalyzer):
    description = "None"

    def process(region_x:list, region_y:list):
        return None


class ValueAnalyzer(BaseAnalyzer):
    description = "Value"

    def process(region_x:list, region_y:list) -> float:
        return region_y[-1]


class MinimumAnalyzer(BaseAnalyzer):
    description = "Minimum"

    def process(region_x:list, region_y:list) -> float:
        import numpy as np
        return np.min(region_y)


class MaximumAnalyzer(BaseAnalyzer):
    description = "Maximum"

    def process(region_x:list, region_y:list) -> float:
        import numpy as np
        return np.max(region_y)


class MeanAnalyzer(BaseAnalyzer):
    description = "Mean"

    def process(region_x:list, region_y:list) -> float:
        import numpy as np
        return np.mean(region_y)


class DetaTAnalyzer(BaseAnalyzer):
    description = "Delta T"

    def process(region_x:list, region_y:list) -> float:
        import numpy as np
        return np.max(region_x) - np.min(region_x)


class PeakPeakAnalyzer(BaseAnalyzer):
    description = "Peak-Peak"

    def process(region_x:list, region_y:list) -> float:
        import numpy as np
        return np.max(region_y) - np.min(region_y)


class IntegrateAnalyzer(BaseAnalyzer):
    description = "Integrate"

    def process(region_x:list, region_y:list) -> float:
        import numpy as np
        return np.trapz(region_y, x=region_x)
