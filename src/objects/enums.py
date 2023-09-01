class EnumString:
    @classmethod
    def list_all(cls):
        return [
            v for k, v in cls.__dict__.items()
            if not k.startswith("__") and isinstance(v, str)
        ]


class AnalyseType(EnumString):
    Minimum = "Minimum"
    Maximum = "Maximum"
    Mean = "Mean"
    DeltaT = "Delta T"
    PeakPeak = "Peak-Peak"
    Integrate = "Integrate"


if __name__ == '__main__':
    print(AnalyseType.list_all())
