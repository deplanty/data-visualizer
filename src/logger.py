import logging
from logging.handlers import RotatingFileHandler
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.widgets import DockJournal


dock_journal: "DockJournal | None" = None


# Configure the logging system
_handler = RotatingFileHandler("data-vizualizer.log", maxBytes=10_000, backupCount=3)  # Octet
_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
_handler.setFormatter(_formatter)

_logger = logging.getLogger("main")
_logger.setLevel(logging.DEBUG)
_logger.addHandler(_handler)


# Methods


def set_journal(widget: "DockJournal"):
    global dock_journal
    dock_journal = widget


# Log levels


def debug(text: str = ""):
    _logger.debug(text)


def info(text: str = ""):
    _logger.info(text)


def warning(text: str = ""):
    _logger.warning(text)


def journal(text: str = ""):
    if dock_journal:
        dock_journal.log(text)
    else:
        debug("logger.journal used but variable `dock_journal` not set")
