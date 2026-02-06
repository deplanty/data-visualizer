import abc
import importlib

from src import logger

from .series import SeriesCollection
from .acquisition import Acquisition


class BaseLoader(abc.ABC):
    file_ext: list[str]
    file_desc: str

    def __init__(self):
        self.data = Acquisition()

    @classmethod
    @abc.abstractmethod
    def load(cls, filename: str) -> SeriesCollection:
        pass

    @classmethod
    def get_file_type(cls):
        return cls.file_desc + " (*." + ", *.".join(cls.file_ext) + ")"


class DataLoader:
    loaders: list[type[BaseLoader]]

    @classmethod
    def init(cls):
        # Import the loaders in the memory
        importlib.import_module("src.objects.loaders")

        # Get the loaders as classes
        cls.loaders = BaseLoader.__subclasses__()

    @classmethod
    def load(cls, filename: str, file_type: str) -> Acquisition:
        """Use the correct loader to read `filename` with the type `file_type`."""

        for loader in cls.loaders:
            if loader.get_file_type() == file_type:
                series = loader.load(filename)
                logger.info(f'Load file "{filename}" with file type "{file_type}"')
                return Acquisition(filename, file_type, series)
        else:
            logger.warning(f'Couldn\'t load "{filename}" with file type "{file_type}"')
            return Acquisition()

    @classmethod
    def list_all_file_type(cls):
        return [loader.get_file_type() for loader in cls.loaders]
