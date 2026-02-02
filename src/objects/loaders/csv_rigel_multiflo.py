from src.objects.data_container import DataContainer
from src.objects.data_loader import BaseLoader


class CsvRigelMultifloLoader(BaseLoader):
    file_ext = ["csv"]
    file_desc = "CSV from Rigel Multiflo"

    @staticmethod
    def load(filename: str) -> DataContainer:
        data = DataContainer()
        data.init(channels=4)

        with open(filename, "r") as fid:

            # 14 lines of useless header
            for _ in range(14):
                fid.readline()
            # Add metadata
            data.x.set(title="Time", unit="sec")
            data.y[0].set(title="Cumulated volume", unit="ml", show=True)
            data.y[1].set(title="Instant flow", unit="ml/h", show=True)
            data.y[2].set(title="Mean flow", unit="ml/h", show=False)
            data.y[3].set(title="Pressure", unit="mmHg", show=False)

            for line in fid:
                line = line.rstrip().split(",")
                # End when the line of the table is empty
                if line[0] == "":
                    break
                # Add the first 5 columns in data
                values = [float(v) for v in line[:5]]
                data.add_row(values, x_index=0)

        return data
