import abc
import glob
import os

from .data_container import DataContainer
from .enums import FileType


class BaseLoader(abc.ABC):
    file_ext: list[str]
    file_desc: str

    def __init__(self):
        self.data = DataContainer()

    @staticmethod
    @abc.abstractmethod
    def load(filename:str) -> DataContainer:
        pass

    @classmethod
    @property
    def file_type(cls):
        return cls.file_desc + " (*." + ", *.".join(cls.file_ext) + ")"



class DataLoader:
    loaders: list[BaseLoader]

    @classmethod
    def init(cls):
        # Get all the loaders as python files
        pyloaders = glob.glob(os.path.join("src", "objects", "loaders", "*.py"))
        for pyfile in pyloaders:
            data = DataContainer()
            with open(pyfile) as fid:
                exec(fid.read())

        # Get the loaders as classes
        cls.loaders = BaseLoader.__subclasses__()

    @classmethod
    def load(cls, filename:str, file_type:str) -> DataContainer:
        for loader in cls.loaders:
            if loader.file_type == file_type:
                break
        else:
            return None

        return loader.load(filename)

    @classmethod
    def list_all_file_type(self):
        return [loader.file_type for loader in cls.loaders]
