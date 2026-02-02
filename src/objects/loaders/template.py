from src.objects.data_container import DataContainer
from src.objects.data_loader import BaseLoader


class CsvTempalceLoader(BaseLoader):
    file_ext = [""]
    file_desc = ""

    @staticmethod
    def load(filename: str) -> DataContainer:
        data = DataContainer()
        data.init(channels=1)

        return data
