import abc
import glob
import os
import importlib


class BaseScript(abc.ABC):
    name: str
    description: str

    @staticmethod
    @abc.abstractmethod
    def process(data, cursor):
        pass


class ScriptsLoader:
    scripts: list[type[BaseScript]]

    @classmethod
    def init(cls):
        # Import all the scripts
        importlib.import_module("src.objects.scripts")

        # Get the loaders as classes
        cls.scripts = BaseScript.__subclasses__()

    @classmethod
    def process(cls, script_name: str, data, cursor):
        for script in cls.scripts:
            if script.name == script_name:
                return script.process(data, cursor)
        else:
            return None

    @classmethod
    def list_all(cls) -> list:
        return [script.name for script in cls.scripts]
