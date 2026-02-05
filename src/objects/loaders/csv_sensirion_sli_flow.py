import re

from src.objects.series import SeriesCollection
from src.objects.data_loader import BaseLoader


def to_float(value: str) -> float:
    # The values are "french style" with a comma as the decimal separator and a space as
    # a separator for thousands.
    # The values are surrounded by ".
    # Example: "1 000,1646" for 1000.1646

    value = value.strip('"')
    value = value.replace(",", ".")
    value = re.sub(r"\s", "", value)
    return float(value)


class CsvSensirionSliLoader(BaseLoader):
    file_ext = ["csv"]
    file_desc = "CSV from Sensirion SLI flow sensor"

    @classmethod
    def load(cls, filename: str) -> SeriesCollection:
        data = SeriesCollection()
        data.init(channels=1)

        sep = ";"
        with open(filename, "r", encoding="utf-8") as fid:
            # The 14 first lines are the header
            for _ in range(14):
                fid.readline()
            # Header
            header = fid.readline().rstrip().split(sep)

            data.x.set(title="Relative Time", unit="s")
            data.y[0].set(title="Flow", unit="µl/min")

            for line in fid:
                line = line.rstrip().split(sep)
                # First line is ignored because its the sample number.

                x = to_float(line[1])
                y = to_float(line[2])
                data.add_row([x, y])

        return data
