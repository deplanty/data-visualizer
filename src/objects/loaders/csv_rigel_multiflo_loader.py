

class CsvRigelMultifloLoader(BaseLoader):
    file_ext = ["csv"]
    file_desc = "CSV from Rigel Multiflo"

    def load(filename:str) -> DataContainer:
        data = DataContainer()

        with open(filename, "r") as fid:
            # 1 (x) + 4 (y) columns of data
            data.init(size=4)

            # 14 lines of useless header
            for _ in range(14): fid.readline()
            # Add metadata
            data.x.set(title = "Time", unit = "sec")
            data.y[0].set(title="Cumulated volume", unit="ml", show=True)
            data.y[1].set(title="Instant flow", unit="ml/h", show=True)
            data.y[2].set(title="Mean flow", unit="ml/h", show=False)
            data.y[3].set(title="Pressure", unit="mmHg", show=False)

            for line in fid:
                line = line.rstrip().split(",")
                # End when empty table line
                if line[0] == "":
                    break
                # Add the 5 columns in data
                data.add_row(line[:5], x_index=0)

        return data
