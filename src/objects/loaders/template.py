from objects.series import SeriesCollection
from src.objects.data_loader import BaseLoader


class CsvTempalceLoader(BaseLoader):
    file_ext = [""]
    file_desc = ""

    @staticmethod
    def load(filename: str) -> SeriesCollection:
        data = SeriesCollection()
        data.init(channels=1)

        return data
