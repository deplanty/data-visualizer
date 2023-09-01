

class CsvCommaLoader(BaseLoader):
    file_ext = ["csv"]
    file_desc = "CSV comma separated values"
    
    def load(self, filename:str) -> DataContainer:
        data = DataContainer()
        # Write here how the data are loaded

        return data
