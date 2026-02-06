from typing import TYPE_CHECKING

# Load the default colors
import src.objects.colors

from src.objects import DataLoader
from src.objects import DataAnalyzer
from src.objects import ScriptsLoader

if TYPE_CHECKING:
    from src.widgets import DockJournal

# Initialize the loaders, analyzers and scripts
DataLoader.init()
DataAnalyzer.init()
ScriptsLoader.init()
