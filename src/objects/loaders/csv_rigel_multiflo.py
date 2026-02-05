from src.objects.series import SeriesCollection
from src.objects.data_loader import BaseLoader


class CsvRigelMultifloLoader(BaseLoader):
    file_ext = ["csv"]
    file_desc = "CSV from Rigel Multiflo"

    @classmethod
    def load(cls, filename: str) -> SeriesCollection:
        data = SeriesCollection()
        data.init(channels=4)

        with open(filename, "r") as fid:

            # 14 lines of useless header
            for _ in range(14):
                fid.readline()
            # Add metadata
            data.x.set(title="Time", unit="sec")
            data.y[0].set(title="Cumulated volume", unit="ml", visible=True)
            data.y[1].set(title="Instant flow", unit="ml/h", visible=True)
            data.y[2].set(title="Mean flow", unit="ml/h", visible=False)
            data.y[3].set(title="Pressure", unit="mmHg", visible=False)

            for line in fid:
                line = line.rstrip().split(",")
                # End when the line of the table is empty
                if line[0] == "":
                    break
                # Add the first 5 columns in data
                values = [float(v) for v in line[:5]]
                data.add_row(values, x_index=0)

        return data
