from src.objects.series import SeriesCollection
from src.objects.data_loader import BaseLoader


class CsvCommaLoader(BaseLoader):
    file_ext = ["csv"]
    file_desc = "CSV comma separated values"

    @staticmethod
    def load(filename: str) -> SeriesCollection:
        sep = ","
        data = SeriesCollection()
        with open(filename, "r") as fid:
            header = fid.readline().rstrip().split(sep)
            channels = len(header) - 1  # First is x axis
            data.init(channels)

            for line in fid:
                line = line.rstrip().split(sep)
                values = [float(v) for v in line]
                data.add_row(values)

            data.x.set(title=header.pop(0))
            for i in range(channels):
                data.y[i].set(title=header[i])

        return data


class CsvTabLoader(BaseLoader):
    file_ext = ["csv"]
    file_desc = "CSV tab separated values"

    @staticmethod
    def load(filename: str) -> SeriesCollection:
        sep = "\t"
        data = SeriesCollection()
        with open(filename, "r") as fid:
            header = fid.readline().rstrip().split(sep)
            channels = len(header) - 1  # First is x axis
            data.init(channels)

            for line in fid:
                line = line.rstrip().split(sep)
                values = [float(v) for v in line]
                data.add_row(values)

            data.x.set(title=header.pop(0))
            for i in range(channels):
                data.y[i].set(title=header[i])

        return data


class CsvSemicolonLoader(BaseLoader):
    file_ext = ["csv"]
    file_desc = "CSV semicolon separated values"

    @staticmethod
    def load(filename: str) -> SeriesCollection:
        sep = ";"
        data = SeriesCollection()
        with open(filename, "r") as fid:
            header = fid.readline().rstrip().split(sep)
            channels = len(header) - 1  # First is x axis
            data.init(channels)

            for line in fid:
                line = line.rstrip().split(sep)
                values = [float(v) for v in line]
                data.add_row(values)

            data.x.set(title=header.pop(0))
            for i in range(channels):
                data.y[i].set(title=header[i])

        return data
