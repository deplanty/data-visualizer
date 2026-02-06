from typing import TYPE_CHECKING

from src.objects.scripts_loader import BaseScript
from src.windows import DialogMultiInput
from src import logger

if TYPE_CHECKING:
    from src.objects import Acquisition, GraphCursor


class SelectTimeScript(BaseScript):
    name = "Select time..."
    description = "Set the cursor at the specified time."

    @classmethod
    def process(cls, acquisition: "Acquisition", cursor: "GraphCursor"):
        dialog = DialogMultiInput()
        dialog.add_input_float("Start time", "s", cursor.start)
        dialog.add_input_float("End time", "s", cursor.end)
        dialog.exec()

        if not dialog.confirmed:
            return

        values = dialog.get_values()
        start = values["Start time"]
        end = values["End time"]
        cursor.set_and_emit(start, end)
        logger.journal(cls.name)
        logger.journal(f" - Start time: {cursor.start}")
        logger.journal(f" - End time: {cursor.end}")
        logger.journal("")
