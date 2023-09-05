import abc
import glob
import os


class BaseAnalyzer(abc.ABC):
    description: str

    @staticmethod
    @abc.abstractmethod
    def process(region_x:list, region_y:list) -> float:
        pass



class DataAnalyzer:
    analyzers: list[BaseAnalyzer]

    @classmethod
    def init(cls):
        # Get all the loaders as python files
        pyloaders = glob.glob(os.path.join("src", "objects", "analyzers", "*.py"))
        for pyfile in pyloaders:
            with open(pyfile) as fid:
                exec(fid.read())

        # Get the loaders as classes
        cls.analyzers = BaseAnalyzer.__subclasses__()

    @classmethod
    def process(cls, analyzer_desc:str, region_x:list, region_y:list) -> float:
        for analyzer in cls.analyzers:
            if analyzer.description == analyzer_desc:
                break
        else:
            return None

        return analyzer.process(region_x, region_y)

    @classmethod
    def list_all(cls):
        return [analyzer.description for analyzer in cls.analyzers]
