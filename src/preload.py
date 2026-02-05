# Load the default colors
import src.objects.colors

from src.objects import DataLoader
from src.objects import DataAnalyzer
from src.objects import ScriptsLoader


DataLoader.init()
DataAnalyzer.init()
ScriptsLoader.init()


logger = None
