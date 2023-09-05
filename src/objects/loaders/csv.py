class CsvCommaLoader(BaseLoader):
    file_ext = ["csv"]
    file_desc = "CSV comma separated values"
    
    def load(filename:str) -> DataContainer:
        sep = ","
        data = DataContainer()
        with open(filename, "r") as fid:
            header = fid.readline().rstrip().split(sep)
            channels = len(header) - 1  # First is x axis
            data.init(channels)

            for line in fid:
                line = line.rstrip().split(sep)
                data.add_row(line)

            data.x.set(title=header.pop(0))
            for i in range(channels):
                data.y[i].set(title=header[i])

        return data


class CsvTabLoader(BaseLoader):
    file_ext = ["csv"]
    file_desc = "CSV tab separated values"

    def load(filename:str) -> DataContainer:
        sep = "\t"
        data = DataContainer()
        with open(filename, "r") as fid:
            header = fid.readline().rstrip().split(sep)
            channels = len(header) - 1  # First is x axis
            data.init(channels)

            for line in fid:
                line = line.rstrip().split(sep)
                data.add_row(line)

            data.x.set(title=header.pop(0))
            for i in range(channels):
                data.y[i].set(title=header[i])

        return data


class CsvSemicolonLoader(BaseLoader):
    file_ext = ["csv"]
    file_desc = "CSV semicolon separated values"

    def load(filename:str) -> DataContainer:
        sep = ";"
        data = DataContainer()
        with open(filename, "r") as fid:
            header = fid.readline().rstrip().split(sep)
            channels = len(header) - 1  # First is x axis
            data.init(channels)

            for line in fid:
                line = line.rstrip().split(sep)
                data.add_row(line)

            data.x.set(title=header.pop(0))
            for i in range(channels):
                data.y[i].set(title=header[i])

        return data
