

class SelectTimeScript(BaseScript):
    name = "Select time..."

    def process(data, cursor):
        from PySide6.QtWidgets import QDialog, QInputDialog
        root = QDialog()
        start, ok_s = QInputDialog.getDouble(root, "Hello", "Label", cursor.start)
        if not ok_s:
            return

        end, ok_e = QInputDialog.getDouble(root, "Hello 2", "Label 2", cursor.start)
        if not ok_e:
            return

        cursor.set_and_emit(start, end)


class GetValuesScript(BaseScript):
    name = "Get values"

    def process(data, cursor):
        print(data, cursor)
