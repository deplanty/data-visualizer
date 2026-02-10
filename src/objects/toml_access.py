import os
import shutil
from typing import Any

import toml


class TomlAccess:
    _path_file: str
    settings: dict

    def __init__(self, filename: str):
        self._path_file = filename

        with open(self._path_file, encoding="utf-8") as fid:
            self._settings = toml.load(fid)

    @classmethod
    def in_userdata(cls, filename: str):
        # Initialize the module by loading the  data in the user data
        path = os.path.expanduser(os.path.join("~", ".data-visualizer", filename))
        if not os.path.exists(path):
            shutil.copyfile(os.path.join("userdata", filename), path)

        return cls(path)

    # Public methods

    def set(self, key: str, value: Any):
        """Set the value for a specific parameter like `"section/subsection/item" = True`"""

        sections = key.split("/")
        tmp = self._settings
        for section in sections[:-1]:
            tmp = tmp[section]
        tmp[sections[-1]] = value
        self.save()

    def get(self, key: str) -> Any:
        """Get the value for a specific parameter like `"section/subsection/item" -> True`"""

        sections = key.split("/")
        tmp = self._settings
        for section in sections:
            tmp = tmp[section]
        return tmp

    def iter_items(self):
        return self._settings.items()

    def save(self):
        with open(self._path_file, "w", encoding="utf-8") as fid:
            toml.dump(self._settings, fid)
