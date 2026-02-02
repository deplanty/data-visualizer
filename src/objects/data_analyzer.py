import abc
import glob
import os
import importlib


class BaseAnalyzer(abc.ABC):
    name: str
    description: str

    @staticmethod
    @abc.abstractmethod
    def process(region_x: list, region_y: list) -> float:
        pass


class DataAnalyzer:
    analyzers: list[type[BaseAnalyzer]]

    @classmethod
    def init(cls):
        # Import all the analyzers
        importlib.import_module("src.objects.analyzers")

        # Get the analyzers
        cls.analyzers = BaseAnalyzer.__subclasses__()

    @classmethod
    def process(cls, analyzer_name: str, region_x: list, region_y: list) -> float:
        for analyzer in cls.analyzers:
            if analyzer.name == analyzer_name:
                return analyzer.process(region_x, region_y)
        else:
            return 0

    @classmethod
    def list_all(cls) -> list[str]:
        return [analyzer.name for analyzer in cls.analyzers]
