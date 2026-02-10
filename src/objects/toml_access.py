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
        # Initialize the settings with the default values
        with open(os.path.join("userdata", filename), encoding="utf-8") as fid:
            default = toml.load(fid)

        path = os.path.expanduser(os.path.join("~", ".data-visualizer", filename))
        # Copy the default values if the user has no userdata
        if not os.path.exists(path):
            shutil.copyfile(os.path.join("userdata", filename), path)
            userdata = cls(path)
        # Update the default values with the user's
        else:
            userdata = cls(path)
            default.update(userdata._settings)
            userdata._settings = default

        return userdata

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
