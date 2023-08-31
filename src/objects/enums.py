class EnumString:
    @classmethod
    def list_all(cls):
        return [
            v for k, v in cls.__dict__.items()
            if not k.startswith("__") and isinstance(v, str)
        ]


class FileType(EnumString):
    RWB_Asl5000 = "ASL5000 raw binary data (*.rwb)"
    CSV_RigelMultiflo = "CSV from Rigel Multiflo (*.csv)"
    CSV_Comma = "CSV Comma separated values (*.csv)"
    CSV_Tab = "CSV Tabulation separated values (*.csv)"
    CSV_Semicolon = "CSV Semicolon separated values (*.csv)"


class AnalyseType(EnumString):
    Minimum = "Minimum"
    Maximum = "Maximum"
    Mean = "Mean"
    DeltaT = "Delta T"
    PeakPeak = "Peak-Peak"
    Integrate = "Integrate"


if __name__ == '__main__':
    print(FileType.list_all())
    print(AnalyseType.list_all())
