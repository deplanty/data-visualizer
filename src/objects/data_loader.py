from .data_container import DataContainer
from .enums import FileType


class DataLoader:
    def __init__(self):
        self.data = DataContainer()

    def load_from_file(self, filename:str, file_type:str):
        if file_type == FileType.CSV_RigelMultiflo:
            self.__load_CSV_RigelMultiflo(filename)

        return self.data

    def __load_CSV_RigelMultiflo(self, filename:str):
        with open(filename, "r") as fid:
            # 1 (x) + 4 (y) columns of data
            self.data.init(size=4)

            # 14 lines of useless header
            for _ in range(14): fid.readline()
            # Add metadata
            self.data.x.title = "Time"
            self.data.x.unit = "sec"
            self.data.y[0].set(title="Cumulated volume", unit="ml", show=True)
            self.data.y[1].set(title="Instant flow", unit="ml/h", show=True)
            self.data.y[2].set(title="Mean flow", unit="ml/h", show=False)
            self.data.y[3].set(title="Pressure", unit="mmHg", show=False)

            for line in fid:
                line = line.rstrip().split(",")
                # End when empty table line
                if line[0] == "":
                    break
                # Add the 5 columns in data
                self.data.add_row(line[:5], x_index=0)


class LoaderDefault:
    file_ext: list[str]
    file_desc: str

    def load(self):
        ...

    @property
    def file_type(self):
        return self.file_desc + " (*." + ", *.".join(self.file_ext) + ")"



class DataContainerLoader:
    def __init__(self):
        import glob
        import os

        loaders = glob.glob(os.path.join(os.path.dirname(__file__), "loaders", "*.py"))
        for pyfile in loaders:
            data = DataContainer()
            with open(pyfile) as fid:
                exec(fid.read(), None, dict(filename="test/dummy.csv", data=data))

        subclasses = LoaderDefault.__subclasses__()
        print(subclasses)
        subc = list()
        for c in subclasses:
            subc.append(c())
        print(subc[0].file_type)


loaders = DataContainerLoader()
