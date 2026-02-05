from dataclasses import dataclass, field
import os

from src.objects import SeriesCollection


@dataclass
class Acquisition:
    """
    The data and metadata of an acquisition.
    """

    path: str = ""
    loader: str = ""
    series: SeriesCollection = field(default_factory=SeriesCollection)

    @property
    def filename(self) -> str:
        """
        The name of the file for this acquisition.

        :return:
        :rtype: str
        """

        return os.path.basename(self.path)

    @property
    def dirname(self) -> str:
        """
        The name of the directory for this acquisition.

        :return:
        :rtype: str
        """

        return os.path.dirname(self.path)
