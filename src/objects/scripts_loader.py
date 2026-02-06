import abc
import importlib
from typing import TYPE_CHECKING

from src import logger

if TYPE_CHECKING:
    from src.objects import Acquisition
    from src.objects import SeriesCollection
    from src.objects import GraphCursor


class BaseScript(abc.ABC):
    name: str
    description: str

    @classmethod
    @abc.abstractmethod
    def _process(cls, acquisition: "Acquisition", cursor: "GraphCursor"):
        pass

    @classmethod
    def process(cls, acquisition: "Acquisition", cursor: "GraphCursor"):
        logger.info(f'Run script "{cls.name}"')
        logger.journal(cls.name)
        cls._process(acquisition, cursor)


class ScriptsLoader:
    scripts: list[type[BaseScript]]

    @classmethod
    def init(cls):
        # Import all the scripts
        importlib.import_module("src.objects.scripts")

        # Get the loaders as classes
        cls.scripts = BaseScript.__subclasses__()

    @classmethod
    def process(cls, script_name: str, data: "Acquisition", cursor: "GraphCursor"):
        for script in cls.scripts:
            if script.name == script_name:
                return script.process(data, cursor)
        else:
            return None

    @classmethod
    def list_all(cls) -> list:
        return [script.name for script in cls.scripts]
