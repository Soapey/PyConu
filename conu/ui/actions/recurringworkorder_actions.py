from PyQt5.QtCore import QDate
from tkinter.messagebox import askyesno
from datetime import datetime, date

from conu.classes.RecurringWorkOrder import RecurringWorkOrder
from conu.classes.UserDepartment import UserDepartment
from conu.classes.RecurringWorkOrderItem import RecurringWorkOrderItem
from conu.classes.Department import Department
from conu.classes.Site import Site
from conu.classes.ItemDepartment import ItemDepartment
from conu.classes.AssigneeDepartment import AssigneeDepartment
from conu.classes.PriorityLevel import PriorityLevel

from conu.classes.User import User
from conu.classes.Item import Item
from conu.classes.Assignee import Assignee

from conu.db.helpers import (
    delete_by_attrs_dict,
    delete_entities_by_ids,
    save_by_list,
    select_by_attrs_dict,
    get_by_user_departments,
)
from conu.helpers import (
    navigate,
    selected_row_id,
    set_button_visibility,
    load_query_rows_into_table,
    load_entities_into_table,
)
from conu.ui.components.Notification import Notification
from conu.ui.components.TableManager import TableManager
from conu.ui.PageEnum import Page
from conu.ui.components.SelectWindow import SelectWindow

unassigned_items_tbl: TableManager = None
assigned_items_tbl: TableManager = None


def load_recurringworkorder_listingview(main_window) -> None:

    main_window.ui.recurringworkorder_listingview_txtSearch.clear()

    recurringworkorders_by_search(main_window, None)

    set_recurringworkorder_button_visibility(main_window)

    navigate(main_window, Page.RECURRINGWORKORDER_LISTINGVIEW)


def clear_recurringworkorder_entryform(main_window) -> None:

    items = get_by_user_departments(Item, main_window.current_user.id)

    main_window.ui.recurringworkorder_entryform_lblId.clear()
    main_window.ui.recurringworkorder_entryform_lblLastRaisedDate.clear()

    main_window.ui.recurringworkorder_entryform_lblSite.clear()
    main_window.ui.recurringworkorder_entryform_lblSite.setProperty("object", None)

    main_window.ui.recurringworkorder_entryform_lblDepartment.clear()
    main_window.ui.recurringworkorder_entryform_lblDepartment.setProperty(
        "object", None
    )

    main_window.ui.recurringworkorder_entryform_lblPriorityLevel.clear()
    main_window.ui.recurringworkorder_entryform_lblPriorityLevel.setProperty(
        "object", None
    )

    main_window.ui.workorder_entryform_txtTaskDescription.clear()
    main_window.ui.workorder_entryform_txtComments.clear()

    global unassigned_items_tbl, assigned_items_tbl

    unassigned_items_tbl = TableManager(
        main_window.ui.recurringworkorder_entryform_tblUnassignedItems, ["ID", "Name"]
    )
    assigned_items_tbl = TableManager(
        main_window.ui.recurringworkorder_entryform_tblAssignedItems, ["ID", "Name"]
    )

    unassigned_items_tbl.clear()
    assigned_items_tbl.clear()

    # TODO - recurrence selection widget clear logic


def new_recurringworkorder(main_window) -> None:

    clear_recurringworkorder_entryform(main_window)

    load_selection_tables(main_window)

    main_window.ui.reccurringworkorder_entryform_txtTaskDescription.setFocus()

    navigate(main_window, Page.RECURRINGWORKORDER_ENTRYFORM)


def edit_recurringworkorder(main_window) -> None:

    sites = select_by_attrs_dict(Site)
    departments = select_by_attrs_dict(Department)
    prioritylevels = select_by_attrs_dict(PriorityLevel)

    selected_id = selected_row_id(
        main_window.ui.recurringworkorder_listingview_tblRecurringWorkOrder
    )
    recurringworkorders = RecurringWorkOrder.get()
    entity = recurringworkorders[selected_id]

    recurringworkorder_site = sites[entity.site_id]
    recurringworkorder_department = departments[entity.department_id]
    recurringworkorder_prioritylevel = prioritylevels[entity.prioritylevel_id]

    clear_recurringworkorder_entryform(main_window)

    main_window.ui.recurringworkorder_entryform_lblId.setText(str(entity.id))

    main_window.ui.recurringworkorder_entryform_lblLastRaisedDate.setText(
        datetime.strftime(entity.lastraised_date, "%d-%m-%Y")
    )

    main_window.ui.recurringworkorder_entryform_lblSite.setProperty(
        "object", recurringworkorder_site
    )
    main_window.ui.recurringworkorder_entryform_lblSite.setText(
        recurringworkorder_site.name
    )

    main_window.ui.recurringworkorder_entryform_lblDepartment.setProperty(
        "object", recurringworkorder_department
    )
    main_window.ui.workorder_entryform_lblDepartment.setText(
        recurringworkorder_department.name
    )

    main_window.ui.recurringworkorder_entryform_lblPriorityLevel.setProperty(
        "object", recurringworkorder_prioritylevel
    )
    main_window.ui.recurringworkorder_entryform_lblPriorityLevel.setText(
        recurringworkorder_prioritylevel.name
    )

    main_window.ui.recurringworkorder_entryform_txtTaskDescription.setPlainText(
        entity.task_description
    )

    if comments := entity.comments:
        main_window.ui.recurringworkorder_entryform_txtComments.setPlainText(comments)

    load_selection_tables(main_window)

    # TODO - recurrence selection widget edit logic.

    main_window.ui.recurringworkorder_entryform_txtTaskDescription.setFocus()

    navigate(main_window, Page.RECURRINGWORKORDER_ENTRYFORM)


def delete_recurringworkorder(main_window) -> None:

    if not askyesno(
        "Confirm delete", "Are you sure you would like to delete the selected record?"
    ):
        return

    selected_id = selected_row_id(
        main_window.ui.recurringworkorder_listingview_tblRecurringWorkOrder
    )

    recurringworkorders = RecurringWorkOrder.get()
    entity = recurringworkorders[selected_id]

    if not entity:
        return

    delete_entities_by_ids(RecurringWorkOrder, [selected_id])

    Notification(
        "Delete Successful",
        [f"Successfully deleted recurring work order: {selected_id}"],
    ).show()

    load_recurringworkorder_listingview(main_window)


def recurringworkorder_entryform_is_valid(main_window) -> bool:

    error_strings = list()

    if not main_window.ui.recurringworkorder_entryform_lblSite.text():
        error_strings.append("A site must be selected.")

    if not main_window.ui.recurringworkorder_entryform_lblDepartment.text():
        error_strings.append("A department must be selected.")

    if not main_window.ui.recurringworkorder_entryform_lblPriorityLevel.text():
        error_strings.append("A priority level must be selected.")

    if not main_window.ui.recurringworkorder_entryform_tblAssignedItems.rowCount() >= 1:
        error_strings.append("At least one item must be assigned.")

    if not main_window.ui.recurringworkorder_entryform_txtTaskDescription.toPlainText():
        error_strings.append("Task Description field cannot be blank.")

    # TODO - recurrence selection widget check if an option has been selected logic

    if error_strings:
        Notification("Cannot Save Recurring Work Order", error_strings).show()

    return not bool(error_strings)


def save_and_delete_recurringworkorderitems(main_window, entity_id):

    existing_item_ids = [
        rwoi.item_id
        for rwoi in select_by_attrs_dict(
            RecurringWorkOrderItem, {"workorder_id": entity_id}
        ).values()
    ]

    assigned_item_ids = list()
    recurringworkorderitems_to_save = list()

    tbl = main_window.ui.recurringworkorder_entryform_tblAssignedItems
    id_column_index = 0

    for row_index in range(tbl.rowCount()):
        _cell = tbl.item(row_index, id_column_index)
        _id = int(_cell.text())
        assigned_item_ids.append(_id)

        if _id not in list(existing_item_ids):
            recurringworkorderitems_to_save.append(
                RecurringWorkOrderItem(None, entity_id, _id)
            )

    for item_id in existing_item_ids:
        if item_id not in assigned_item_ids:
            delete_by_attrs_dict(
                RecurringWorkOrderItem,
                {"recurringworkorder_id": entity_id, "item_id": item_id},
            )

    save_by_list(recurringworkorderitems_to_save)


def save_recurringworkorder(main_window) -> None:

    if not recurringworkorder_entryform_is_valid(main_window):
        return

    if not askyesno(
        "Confirm save", "Are you sure you would like to save the current record?"
    ):
        return

    entity_id = (
        None
        if len(main_window.ui.recurringworkorder_entryform_lblId.text()) == 0
        else int(main_window.ui.recurringworkorder_entryform_lblId.text())
    )

    selected_site = main_window.ui.recurringworkorder_entryform_lblSite.property(
        "object"
    )
    selected_department = (
        main_window.ui.recurringworkorder_entryform_lblDepartment.property("object")
    )
    selected_prioritylevel = (
        main_window.ui.recurringworkorder_entryform_lblPriorityLevel.property("object")
    )
    close_out_comments = (
        None
        if not main_window.ui.workorder_entryform_chkIsComplete.isChecked()
        else main_window.ui.workorder_entryform_txtCloseOutComments.toPlainText()
    )

    # TODO - Instantiate entity = RecurringWorkOrder()
    entity = RecurringWorkOrder()

    entity_id = sorted(save_by_list([entity]), key=lambda e: e.id, reverse=True)[0].id

    save_and_delete_recurringworkorderitems(main_window, entity_id)

    Notification(
        "Save Successful", [f"Successfully saved recurring work order: {entity_id}"]
    ).show()

    load_recurringworkorder_listingview(main_window)

    clear_recurringworkorder_entryform(main_window)


def back_to_recurringworkorder_listingview(main_window) -> None:

    clear_recurringworkorder_entryform(main_window)

    navigate(main_window, Page.RECURRINGWORKORDER_LISTINGVIEW)


def recurringworkorders_by_search(main_window, search_text: str) -> None:

    recurringworkorder_table_data = RecurringWorkOrder.get_listingview_table_data(
        main_window
    )

    if not search_text:
        matches = recurringworkorder_table_data
    else:
        matches = list(
            filter(
                lambda tup: search_text
                in "".join(
                    [
                        str(tup[0]),
                        tup[1],
                        tup[2],
                        tup[4],
                        tup[5],
                        tup[7],
                    ]
                ).lower(),
                recurringworkorder_table_data,
            )
        )

    load_query_rows_into_table(
        main_window.ui.workorder_listingview_tblWorkOrder,
        matches,
        {
            "ID": (0, str),
            "Site": (1, None),
            "Department": (2, None),
            "Priority Level": (3, None),
            "Task Description": (4, None),
            "Comments": (5, None),
            "Recurrence": (6, None),
            "Due": (7, str),
        },
    )


def set_recurringworkorder_button_visibility(main_window):

    if main_window.current_user.permission_level <= 1:
        set_button_visibility(
            [
                main_window.ui.recurringworkorder_listingview_btnNew,
                main_window.ui.recurringworkorder_listingview_btnEdit,
                main_window.ui.recurringworkorder_listingview_btnDelete,
            ],
            is_visible=False,
        )
    else:
        set_button_visibility(
            [main_window.ui.recurringworkorder_listingview_btnNew], is_visible=True
        )
        set_button_visibility(
            [
                main_window.ui.recurringworkorder_listingview_btnEdit,
                main_window.ui.recurringworkorder_listingview_btnDelete,
            ],
            is_visible=selected_row_id(
                main_window.ui.recurringworkorder_listingview_tblRecurringWorkOrder
            )
            is not None,
        )


def transfer_item_to_table(from_table: TableManager, to_table: TableManager):

    selected_item = from_table.first_selected_item()

    if not selected_item:
        return

    selected_row = selected_item.row()
    selected_id = int(selected_item.text())

    items = select_by_attrs_dict(Item)
    selected_entity = items[selected_id]

    from_table.remove_row(selected_row)

    to_table.add_row()

    to_table.set_item(to_table.last_row_index, 0, str(selected_id))
    to_table.set_item(to_table.last_row_index, 1, selected_entity.name)


def select_site(main_window):

    sites = select_by_attrs_dict(Site)

    SelectWindow(
        sites,
        main_window.ui.recurringworkorder_entryform_lblSite.setText,
        "name",
        main_window.ui.recurringworkorder_entryform_lblSite.setProperty,
        {"id": "ID", "name": "Name"},
    )


def select_department(main_window):

    departments = main_window.current_user.get_departments()

    SelectWindow(
        departments,
        main_window.ui.recurringworkorder_entryform_lblDepartment.setText,
        "name",
        main_window.ui.recurringworkorder_entryform_lblDepartment.setProperty,
        {"id": "ID", "name": "Name"},
        lambda: load_selection_tables(main_window),
    )


def select_prioritylevel(main_window):

    prioritylevels = select_by_attrs_dict(PriorityLevel)

    SelectWindow(
        prioritylevels,
        main_window.ui.recurringworkorder_entryform_lblPriorityLevel.setText,
        "name",
        main_window.ui.recurringworkorder_entryform_lblPriorityLevel.setProperty,
        {"id": "ID", "name": "Name", "days_until_overdue": "Days Until Overdue"},
    )


def load_item_selection_table(main_window):

    id = main_window.ui.recurringworkorder_entryform_lblId.text()

    department = main_window.ui.recurringworkorder_entryform_lblDepartment.property(
        "object"
    )

    global unassigned_items_tbl, assigned_items_tbl
    unassigned_items_tbl.clear()
    assigned_items_tbl.clear()

    if department is None:
        return

    all_items = select_by_attrs_dict(Item)

    item_departments = select_by_attrs_dict(
        ItemDepartment, {"department_id": department.id}
    ).values()

    items = [all_items[item_id] for item_id in {id.item_id for id in item_departments}]

    items = sorted(items, key=lambda e: e.name)

    if id is None or len(id) == 0:
        load_entities_into_table(
            unassigned_items_tbl.table, items, {"id": "ID", "name": "Name"}
        )
        return

    id = int(id)

    recurringworkorder_items = select_by_attrs_dict(
        RecurringWorkOrderItem, {"recurringworkorder_id": id}
    )
    assigned_item_ids = [rwoi.item_id for rwoi in recurringworkorder_items.values()]

    unassigned_items = [item for item in items if item.id not in assigned_item_ids]
    assigned_items = [all_items[item_id] for item_id in assigned_item_ids]

    load_entities_into_table(
        unassigned_items_tbl.table, unassigned_items, {"id": "ID", "name": "Name"}
    )
    load_entities_into_table(
        assigned_items_tbl.table, assigned_items, {"id": "ID", "name": "Name"}
    )


def load_selection_tables(main_window):

    load_item_selection_table(main_window)


def connect_workorder_actions(main_window) -> None:

    global unassigned_items_tbl, assigned_items_tbl

    main_window.ui.action_recurringworkorders.triggered.connect(
        lambda: load_recurringworkorder_listingview(main_window)
    )
    main_window.ui.recurringworkorder_listingview_btnNew.clicked.connect(
        lambda: new_recurringworkorder(main_window)
    )
    main_window.ui.recurringworkorder_listingview_btnEdit.clicked.connect(
        lambda: edit_recurringworkorder(main_window)
    )
    main_window.ui.recurringworkorder_listingview_btnDelete.clicked.connect(
        lambda: delete_recurringworkorder(main_window)
    )
    main_window.ui.recurringworkorder_entryform_btnSave.clicked.connect(
        lambda: save_recurringworkorder(main_window)
    )
    main_window.ui.recurringworkorder_entryform_btnBack.clicked.connect(
        lambda: back_to_recurringworkorder_listingview(main_window)
    )
    main_window.ui.recurringworkorder_entryform_btnSelectSite.clicked.connect(
        lambda: select_site(main_window)
    )
    main_window.ui.recurringworkorder_entryform_btnSelectDepartment.clicked.connect(
        lambda: select_department(main_window)
    )
    main_window.ui.recurringworkorder_entryform_btnSelectPriorityLevel.clicked.connect(
        lambda: select_prioritylevel(main_window)
    )
    main_window.ui.recurringworkorder_entryform_btnAssignItemToWorkOrder.clicked.connect(
        lambda: transfer_item_to_table(unassigned_items_tbl, assigned_items_tbl)
    )
    main_window.ui.recurringworkorder_entryform_btnUnassignItemFromWorkOrder.clicked.connect(
        lambda: transfer_item_to_table(assigned_items_tbl, unassigned_items_tbl)
    )
    main_window.ui.recurringworkorder_listingview_txtSearch.textChanged.connect(
        lambda: recurringworkorders_by_search(
            main_window, main_window.ui.workorder_listingview_txtSearch.text().lower()
        )
    )
    main_window.ui.recurringworkorder_listingview_tblRecurringWorkOrder.itemSelectionChanged.connect(
        lambda: set_recurringworkorder_button_visibility(main_window)
    )
