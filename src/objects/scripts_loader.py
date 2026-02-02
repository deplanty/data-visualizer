import abc
import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.objects.data_container import DataContainer
    from src.objects.cursor import Cursor


class BaseScript(abc.ABC):
    name: str
    description: str

    @staticmethod
    @abc.abstractmethod
    def process(data: "DataContainer", cursor: "Cursor"):
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
