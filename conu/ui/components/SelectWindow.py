from PyQt5.QtWidgets import QMainWindow, QAbstractItemView
from conu.ui.components.Ui_SelectWindow import Ui_SelectWindow
from conu.helpers import selected_row_id, load_entities_into_table
from conu.classes.Form import Form
import win32com.client as win32
import os


class SelectWindow(QMainWindow):
    def __init__(
        self,
        entities,
        set_value_func,
        entity_attribute_name_to_set_value,
        set_property_func,
        headers_dict: dict,
        func_on_exit=None,
        selection_mode: QAbstractItemView.SelectionMode = QAbstractItemView.SelectionMode.SingleSelection,
        printing_workorder=None,
    ) -> None:
        super().__init__()
        self.entities = entities
        self.set_value_func = set_value_func
        self.entity_attribute_name_to_set_value = entity_attribute_name_to_set_value
        self.set_property_func = set_property_func
        self.headers_dict = headers_dict
        self.selection_mode = selection_mode
        self.func_on_exit = func_on_exit
        self.printing_workorder = printing_workorder
        self.ui = Ui_SelectWindow()
        self.ui.setupUi(self)
        self._connect_select_actions()
        self._clear()

    def _load(self):

        self._entities_by_search(None)

        self.ui.selectwindow_tblSelect.setSelectionMode(self.selection_mode)

        self.showMaximized()

    def _clear(self):

        self.ui.selectwindow_txtSearch.clear()

        self._load()

    def _get_selected_entities(self):

        tbl = self.ui.selectwindow_tblSelect

        selected_entities = list()
        if self.selection_mode == QAbstractItemView.SelectionMode.SingleSelection:
            selected_id = selected_row_id(tbl)

            if not selected_id:
                return

            entity = self.entities[selected_id]

            set_value_value = getattr(entity, self.entity_attribute_name_to_set_value)
            if self.set_value_func:
                self.set_value_func(set_value_value)
            if self.set_property_func:
                self.set_property_func("object", entity)

        else:
            selected_items = tbl.selectedItems()

            if not selected_items:
                return

            for item in selected_items:
                if item.column() == 0:
                    entity = self.entities[int(item.text())]
                    selected_entities.append(entity)

            if self.set_value_func:
                self.set_value_func(selected_entities)

        return selected_entities

    def _select(self):

        if self.printing_workorder:

            self.printing_workorder.save(print_on_save=True)

            selected_form: Form
            word = None
            excel = None
            for selected_form in self._get_selected_entities():

                if os.path.exists(selected_form.path):
                    if ".doc" in selected_form.path:
                        # Open Word application
                        word = win32.Dispatch("Word.Application")
                        path_sections = selected_form.path.split("/")
                        drive = path_sections[0]
                        directories = selected_form.path.split("/")[1:]
                        word_path = os.path.join(drive, os.sep, *directories)
                        doc = word.Documents.Open(word_path)
                        doc.PrintOut()
                        doc.Close()
                    elif ".xls" in selected_form.path:
                        excel = win32.Dispatch("Excel.Application")
                        workbook = excel.Workbooks.Open(selected_form.path)
                        workbook.PrintOut()
                        workbook.Close()

            if word:
                if word.Documents.Count == 0:
                    word.Quit()

            if excel:
                if excel.Workbooks.Count == 0:
                    excel.Quit()

        else:
            self._get_selected_entities()

            if self.func_on_exit:
                self.func_on_exit()

        self.close()

    def _entities_by_search(self, search_text: str):

        if not search_text:
            matches = list(self.entities.values())
        else:
            matches = [
                e
                for e in self.entities.values()
                if search_text
                in "".join(
                    [
                        str(getattr(e, attr_name)).lower()
                        for attr_name in self.headers_dict.keys()
                    ]
                )
            ]

        load_entities_into_table(
            self.ui.selectwindow_tblSelect, matches, self.headers_dict
        )

    def _connect_select_actions(self):
        self.ui.selectwindow_btnSelect.clicked.connect(lambda: self._select())
        self.ui.selectwindow_txtSearch.textChanged.connect(
            lambda: self._entities_by_search(
                self.ui.selectwindow_txtSearch.text().lower()
            )
        )
