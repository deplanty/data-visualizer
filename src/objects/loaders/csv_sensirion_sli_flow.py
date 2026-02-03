from src.objects.series import SeriesCollection
from src.objects.data_loader import BaseLoader


class CsvSensirionSliLoader(BaseLoader):
    file_ext = ["csv"]
    file_desc = "CSV from Sensirion SLI flow sensor"

    @staticmethod
    def load(filename: str) -> SeriesCollection:
        data = SeriesCollection()
        data.init(channels=1)

        sep = ";"
        with open(filename, "r") as fid:
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
                # The values are "french style" with a comma as the decimal separator.
                # The values are surrounded by \"
                x = float(line[1].strip('"').replace(",", "."))
                y = float(line[2].strip('"').replace(",", "."))
                data.add_row([x, y])

        return data
