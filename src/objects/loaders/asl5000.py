from src.objects.data_container import DataContainer
from src.objects.data_loader import BaseLoader


class Asl5000Loader(BaseLoader):
    file_ext = ["rwb"]
    file_desc = "ASL5000 raw binary data"

    @staticmethod
    def load(filename: str) -> DataContainer:
        data = DataContainer()
        data.init(channels=12)

        import asl5000_utils as asl

        _labels, array = asl.read_rwb(filename)
        data.x.set(values=array.pop(0), title="Time", unit="sec")
        for i in range(12):
            data.y[i].set(values=array[i])

        data.y[0].set(title="Airway Pressure", unit="cmH2O", show=True)
        data.y[1].set(title="Muscle Pressure", unit="cmH2O", show=True)
        data.y[2].set(title="Tracheal Pressure", unit="cmH2O", show=False)
        data.y[3].set(title="Chamber 1 Volume", unit="L", show=False)
        data.y[4].set(title="Chamber 2 Volume", unit="L", show=False)
        data.y[5].set(title="Total Volume", unit="L", show=True)
        data.y[6].set(title="Chamber 1 Pressure", unit="cmH2O", show=False)
        data.y[7].set(title="Chamber 2 Pressure", unit="cmH2O", show=False)
        data.y[8].set(title="Breath File Number", unit="#", show=False)
        data.y[9].set(title="Aux 1", unit="V", show=False)
        data.y[10].set(title="Aux 2", unit="V", show=False)
        data.y[11].set(title="Oxygen Sensor", unit="V", show=False)

        return data
