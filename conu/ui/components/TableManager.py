from PyQt5.QtWidgets import QTableWidgetItem


class TableManager:
    def __init__(self, table, headers):

        self.table = table
        self.headers = headers
        self.last_row_index = None
        self.clear()

    def set_row_count(self, row_count: int):
        self.table.setRowCount(row_count)
        self.last_row_index = row_count - 1

    def clear(self):
        self.table.clear()
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.set_row_count(0)
        self.last_row_index = 0

    def add_row(self):
        self.set_row_count(self.table.rowCount() + 1)

    def remove_row(self, row_index: int):
        self.table.removeRow(row_index)

    def set_item(self, row_index: int, column_index: int, value: str):

        self.table.setItem(row_index, column_index, QTableWidgetItem(value))

    def selected_items(self):
        return self.table.selectedItems()

    def first_selected_item(self):

        selected_items = self.selected_items()

        if not selected_items:
            return None

        return selected_items[0]
