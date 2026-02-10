import os
from typing import TYPE_CHECKING

# Load the default colors
import src.objects.colors
from src.objects import DataLoader, DataAnalyzer, ScriptsLoader
from src.objects.toml_access import TomlAccess

if TYPE_CHECKING:
    from src.widgets import DockJournal


def init_env():
    # Initialize the folder where the user data are stored
    default_dir = os.path.expanduser(os.path.join("~", ".data-visualizer"))
    os.makedirs(default_dir, exist_ok=True)

    # Initialize the loaders, analyzers and scripts
    DataLoader.init()
    DataAnalyzer.init()
    ScriptsLoader.init()


init_env()

settings = TomlAccess.in_userdata("settings.toml")
