from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox
from tkinter.messagebox import askyesno

from conu.classes.Item import Item
from conu.classes.ItemDepartment import ItemDepartment
from conu.classes.Department import Department
from conu.db.helpers import (
    delete_by_attrs_dict,
    get_by_user_departments,
    save_by_list,
    select_by_attrs_dict,
)
from conu.helpers import (
    clear_widget_children,
    load_entities_into_table,
    navigate,
    selected_row_id,
    set_button_visibility,
)
from conu.ui.components.Notification import SuccessNotification, ErrorNotification
from conu.ui.PageEnum import Page


item_department_ids = set()


def load_item_listingview(main_window) -> None:

    global global_items
    global_items = get_by_user_departments(Item, main_window.current_user.id)

    main_window.ui.item_listingview_txtSearch.clear()

    items_by_search(main_window, None)

    set_item_button_visibility(main_window)

    navigate(main_window, Page.ITEM_LISTINGVIEW)


def clear_item_entryform(main_window, item_id: int = None) -> None:

    main_window.ui.item_entryform_lblId.clear()
    main_window.ui.item_entryform_txtName.clear()
    main_window.ui.item_entryform_txtComments.clear()

    vboxDepartments = (
        main_window.ui.item_entryform_vboxDepartments
    )  # Get item departments vertical box layout
    vboxDepartments.setAlignment(Qt.AlignTop)

    clear_widget_children(vboxDepartments)

    # Retrieve global_departments and global_itemdepartments using select_by_attrs_dict function
    global global_departments
    global global_itemdepartments
    global_departments = select_by_attrs_dict(Department)
    global_itemdepartments = select_by_attrs_dict(ItemDepartment)

    # Create a set to store the IDs of departments assigned to the item, if an item ID has been provided
    global item_department_ids
    if item_id:
        item_department_ids = {
            id.department_id
            for id in global_itemdepartments.values()
            if id.item_id == item_id
        }
    else:
        item_department_ids = set()

    # Loop through each department and create a QCheckBox widget for it
    for department in list(global_departments.values()):

        # Create a QCheckBox widget with the department name and add it to the vbox_departments layout
        checkbox = QCheckBox(department.name, main_window.ui.page_item_entryform)
        checkbox.setProperty("object", department)
        checkbox.setChecked(False)  # Set the checkbox to unchecked by default

        # Check if the department is assigned to the item, and if so, set the checkbox to checked
        if department.id in item_department_ids:
            checkbox.setChecked(True)

        # Add the checkbox widget to the vbox_departments layout
        vboxDepartments.addWidget(checkbox)


def new_item(main_window) -> None:

    clear_item_entryform(main_window)

    main_window.ui.item_entryform_txtName.setFocus()

    navigate(main_window, Page.ITEM_ENTRYFORM)


def edit_item(main_window) -> None:

    selected_id = selected_row_id(main_window.ui.item_listingview_tblItem)
    global global_items
    entity = global_items[selected_id]

    clear_item_entryform(main_window, selected_id)

    main_window.ui.item_entryform_lblId.setText(str(entity.id))
    main_window.ui.item_entryform_txtName.setText(entity.name)
    main_window.ui.item_entryform_txtComments.setPlainText(entity.comments)
    main_window.ui.item_entryform_txtName.setFocus()

    navigate(main_window, Page.ITEM_ENTRYFORM)


def delete_item(main_window) -> None:

    if not askyesno(
        "Confirm delete", "Are you sure you would like to delete the selected record?"
    ):
        return

    selected_id = selected_row_id(main_window.ui.item_listingview_tblItem)
    global global_items
    entity = global_items[selected_id]

    delete_by_attrs_dict(Item, {"id": entity.id})

    SuccessNotification(
        "Delete Successful", [f"Successfully deleted item: {entity.name}"]
    ).show()

    load_item_listingview(main_window)


def item_entryform_is_valid(main_window) -> bool:

    error_strings = list()

    name = main_window.ui.item_entryform_txtName.text()
    if not name:
        error_strings.append("Name field cannot be blank.")
    else:
        existing_items = select_by_attrs_dict(Item, {"name": name})
        editing_id = main_window.ui.item_entryform_lblId.text()

        if existing_items and editing_id:

            existing_item = list(existing_items.values())[0]

            if existing_item.id != int(editing_id):
                error_strings.append(f"Item: {name}, already exists.")

    vboxDepartments = main_window.ui.item_entryform_vboxDepartments
    if not any(
        [
            vboxDepartments.itemAt(i).widget().isChecked()
            for i in range(vboxDepartments.count())
        ]
    ):
        error_strings.append("At least one department must be selected.")

    if error_strings:
        ErrorNotification("Cannot Save Item", error_strings).show()

    return not bool(error_strings)


def save_and_delete_itemdepartments(main_window, entity_id):

    itemdepartments_to_save = list()
    vboxDepartments = main_window.ui.item_entryform_vboxDepartments
    for i in range(vboxDepartments.count()):
        widget = vboxDepartments.itemAt(i).widget()
        if isinstance(widget, QCheckBox):
            department = widget.property("object")

            if widget.isChecked():

                if department.id not in item_department_ids:
                    itemdepartments_to_save.append(
                        ItemDepartment(None, entity_id, department.id)
                    )

            else:

                if department.id in item_department_ids:
                    delete_by_attrs_dict(
                        ItemDepartment,
                        {"item_id": entity_id, "department_id": department.id},
                    )

    save_by_list(itemdepartments_to_save)


def save_item(main_window) -> None:

    if not item_entryform_is_valid(main_window):
        return

    if not askyesno(
        "Confirm save", "Are you sure you would like to save the current record?"
    ):
        return

    entity = Item(
        None
        if len(main_window.ui.item_entryform_lblId.text()) == 0
        else int(main_window.ui.item_entryform_lblId.text()),
        main_window.ui.item_entryform_txtName.text(),
        main_window.ui.item_entryform_txtComments.toPlainText(),
    )

    entity_id = sorted(save_by_list([entity]), key=lambda e: e.id, reverse=True)[0].id

    save_and_delete_itemdepartments(main_window, entity_id)

    SuccessNotification(
        "Save Successful", [f"Successfully saved item: {entity.name}"]
    ).show()

    load_item_listingview(main_window)

    clear_item_entryform(main_window)


def back_to_item_listingview(main_window) -> None:

    clear_item_entryform(main_window)

    navigate(main_window, Page.ITEM_LISTINGVIEW)


def items_by_search(main_window, search_text: str) -> None:

    global global_items

    if not search_text:
        matches = list(global_items.values())
    else:
        matches = list(
            filter(
                lambda e: search_text in "".join([str(e.id), e.name.lower()]),
                global_items.values(),
            )
        )

    load_entities_into_table(
        main_window.ui.item_listingview_tblItem,
        matches,
        {"id": "ID", "name": "Name", "comments": "Comments"},
    )


def set_item_button_visibility(main_window):

    if main_window.current_user.permission_level <= 1:
        set_button_visibility(
            [
                main_window.ui.item_listingview_btnNew,
                main_window.ui.item_listingview_btnEdit,
                main_window.ui.item_listingview_btnDelete,
            ],
            is_visible=False,
        )
    else:
        set_button_visibility([main_window.ui.item_listingview_btnNew], is_visible=True)
        set_button_visibility(
            [
                main_window.ui.item_listingview_btnEdit,
                main_window.ui.item_listingview_btnDelete,
            ],
            is_visible=selected_row_id(main_window.ui.item_listingview_tblItem)
            is not None,
        )


def connect_item_actions(main_window) -> None:

    main_window.ui.action_items.triggered.connect(
        lambda: load_item_listingview(main_window)
    )
    main_window.ui.item_listingview_btnNew.clicked.connect(
        lambda: new_item(main_window)
    )
    main_window.ui.item_listingview_btnEdit.clicked.connect(
        lambda: edit_item(main_window)
    )
    main_window.ui.item_listingview_btnDelete.clicked.connect(
        lambda: delete_item(main_window)
    )
    main_window.ui.item_entryform_btnSave.clicked.connect(
        lambda: save_item(main_window)
    )
    main_window.ui.item_entryform_btnBack.clicked.connect(
        lambda: back_to_item_listingview(main_window)
    )
    main_window.ui.item_listingview_txtSearch.textChanged.connect(
        lambda: items_by_search(
            main_window, main_window.ui.item_listingview_txtSearch.text().lower()
        )
    )
    main_window.ui.item_listingview_tblItem.itemSelectionChanged.connect(
        lambda: set_item_button_visibility(main_window)
    )
