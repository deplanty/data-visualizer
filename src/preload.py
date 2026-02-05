from typing import TYPE_CHECKING

# Load the default colors
import src.objects.colors

from src.objects import DataLoader
from src.objects import DataAnalyzer
from src.objects import ScriptsLoader

if TYPE_CHECKING:
    from src.widgets import DockJournal

DataLoader.init()
DataAnalyzer.init()
ScriptsLoader.init()


logger: "DockJournal | None" = None


def log(text: str):
    if logger:
        logger.log(text)
