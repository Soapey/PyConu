from PyQt5.QtWidgets import QMainWindow
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
    ) -> None:
        super().__init__()
        self.entities = entities
        self.set_value_func = set_value_func
        self.entity_attribute_name_to_set_value = entity_attribute_name_to_set_value
        self.set_property_func = set_property_func
        self.headers_dict = headers_dict
        self.ui = Ui_SelectWindow()
        self.ui.setupUi(self)
        self._connect_select_actions()
        self._clear()

    def _load(self):

        self._entities_by_search(None)

        self.showMaximized()

    def _clear(self):

        self.ui.selectwindow_txtSearch.clear()

        self._load()

    def _select(self):

        selected_id = selected_row_id(self.ui.selectwindow_tblSelect)

        if not selected_id:
            return

        selected_entity = self.entities[selected_id]

        set_value_value = getattr(
            selected_entity, self.entity_attribute_name_to_set_value
        )
        self.set_value_func(set_value_value)
        self.set_property_func("object", selected_entity)

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
