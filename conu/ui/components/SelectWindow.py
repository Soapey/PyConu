from PyQt5.QtWidgets import QMainWindow, QAbstractItemView
from conu.ui.components.Ui_SelectWindow import Ui_SelectWindow
from conu.helpers import selected_row_id, load_entities_into_table


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
    ) -> None:
        super().__init__()
        self.entities = entities
        self.set_value_func = set_value_func
        self.entity_attribute_name_to_set_value = entity_attribute_name_to_set_value
        self.set_property_func = set_property_func
        self.headers_dict = headers_dict
        self.selection_mode = selection_mode
        self.func_on_exit = func_on_exit
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
            self.set_value_func(set_value_value)
            self.set_property_func("object", entity)

        else:
            selected_ranges = tbl.selectedRanges()

            if not selected_ranges:
                return

            for range in selected_ranges:
                for row in range(range.topRow(), range.bottomRow() + 1):
                    entity = self.entities[row[0]]
                    selected_entities.append(entity)

            self.set_value_func(selected_entities)

    def _select(self):

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
