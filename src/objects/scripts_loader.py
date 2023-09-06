import abc
import glob
import os


class BaseScript(abc.ABC):
    name: str

    @staticmethod
    @abc.abstractmethod
    def process(data, cursor):
        pass


class ScriptsLoader:
    scripts: list[BaseScript]

    @classmethod
    def init(cls):
        # Get all the loaders as python files
        pyscript = glob.glob(os.path.join("src", "objects", "scripts", "*.py"))
        for pyfile in pyscript:
            with open(pyfile) as fid:
                exec(fid.read())

        # Get the loaders as classes
        cls.scripts = BaseScript.__subclasses__()

    @classmethod
    def process(cls, script_name:str, data, cursor) -> float:
        for script in cls.scripts:
            if script.name == script_name:
                break
        else:
            return None

        return script.process(data, cursor)

    @classmethod
    def list_all(cls) -> list:
        return [script.name for script in cls.scripts]
