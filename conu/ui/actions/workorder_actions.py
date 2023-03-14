from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QDate
from tkinter.messagebox import askyesno
from datetime import datetime, date

from conu.classes.WorkOrder import WorkOrder
from conu.classes.UserDepartment import UserDepartment
from conu.classes.WorkOrderAssignee import WorkOrderAssignee
from conu.classes.WorkOrderItem import WorkOrderItem
from conu.classes.Department import Department
from conu.classes.Site import Site
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
from conu.db.SQLiteConnection import SQLiteConnection
from conu.ui.components.Notification import Notification
from conu.ui.PageEnum import Page
from conu.ui.components.SelectWindow import SelectWindow


def load_workorder_listingview(main_window) -> None:

    global global_users
    global global_sites
    global global_departments
    global global_prioritylevels
    global global_workorders
    global workorder_table_data

    global_users = select_by_attrs_dict(User)
    global_sites = select_by_attrs_dict(Site)
    global_departments = select_by_attrs_dict(Department)
    global_prioritylevels = select_by_attrs_dict(PriorityLevel)

    user_department_ids = [
        e.department_id
        for e in select_by_attrs_dict(
            UserDepartment, {"user_id": main_window.current_user.id}
        ).values()
    ]

    global_workorders = filter(
        lambda _, e: e.department_id in user_department_ids,
        select_by_attrs_dict(WorkOrder).items(),
    )

    workorder_table_data = WorkOrder.get_listingview_table_data(main_window)

    main_window.ui.workorder_listingview_txtSearch.clear()

    workorders_by_search(main_window, None)

    set_workorder_button_visibility(main_window)

    navigate(main_window, Page.WORKORDER_LISTINGVIEW)


def clear_workorder_entryform(main_window) -> None:

    global global_items
    global global_assignees

    global_items = get_by_user_departments(Item, main_window.current_user.id)
    global_assignees = get_by_user_departments(Assignee, main_window.current_user.id)

    main_window.ui.workorder_entryform_lblId.clear()
    main_window.ui.workorder_entryform_lblDateCreated.clear()

    main_window.ui.workorder_entryform_lblRaisedBy.clear()
    main_window.ui.workorder_entryform_lblRaisedBy.setProperty("object", None)

    main_window.ui.workorder_entryform_lblSite.clear()
    main_window.ui.workorder_entryform_lblSite.setProperty("object", None)

    main_window.ui.workorder_entryform_lblDepartment.clear()
    main_window.ui.workorder_entryform_lblDepartment.setProperty("object", None)

    main_window.ui.workorder_entryform_lblPriorityLevel.clear()
    main_window.ui.workorder_entryform_lblPriorityLevel.setProperty("object", None)

    main_window.ui.workorder_entryform_txtPurchaseOrderNumber.clear()
    main_window.ui.workorder_entryform_txtTaskDescription.clear()
    main_window.ui.workorder_entryform_txtComments.clear()

    main_window.ui.workorder_entryform_dteDateAllocated.setDate(QDate(2000, 1, 1))
    main_window.ui.workorder_entryform_chkIsComplete.setChecked(False)

    main_window.ui.workorder_entryform_dteDateCompleted.setDate(QDate(2000, 1, 1))
    main_window.ui.workorder_entryform_dteDateCompleted.setEnabled(False)

    main_window.ui.workorder_entryform_txtCloseOutComments.clear()
    main_window.ui.workorder_entryform_txtCloseOutComments.setEnabled(False)

    main_window.ui.workorder_entryform_tblUnassignedItems.clear()
    main_window.ui.workorder_entryform_tblAssignedItems.clear()
    main_window.ui.workorder_entryform_tblUnassignedAssignees.clear()
    main_window.ui.workorder_entryform_tblAssignedAssignees.clear()


def new_workorder(main_window) -> None:

    clear_workorder_entryform(main_window)

    main_window.ui.workorder_entryform_txtPurchaseOrderNumber.setFocus()

    navigate(main_window, Page.WORKORDER_ENTRYFORM)


def edit_workorder(main_window) -> None:

    global global_workorders
    global global_users
    global global_sites
    global global_departments
    global global_prioritylevels
    global global_items
    global global_assignees

    selected_id = selected_row_id(main_window.ui.workorder_listingview_tblWorkOrder)
    entity = global_workorders[selected_id]

    workorder_site = global_sites[entity.site_id]
    workorder_department = global_departments[entity.department_id]
    workorder_prioritylevel = global_prioritylevels[entity.prioritylevel_id]
    workorder_raisedby_user = global_users[entity.raisedby_user_id]

    clear_workorder_entryform(main_window, selected_id)

    main_window.ui.workorder_entryform_lblId.setText(str(entity.id))

    main_window.ui.workorder_entryform_lblDateCreated.setText(
        datetime.strftime(entity.date_created, "%d-%m-%Y")
    )

    main_window.ui.workorder_entryform_lblRaisedBy.setText(
        f"{workorder_raisedby_user.first_name} {workorder_raisedby_user.last_name}"
    )
    main_window.ui.workorder_entryform_lblRaisedBy.setProperty(
        "object", workorder_raisedby_user
    )

    main_window.ui.workorder_entryform_lblSite.setText(workorder_site.name)
    main_window.ui.workorder_entryform_lblSite.setProperty("object", workorder_site)

    main_window.ui.workorder_entryform_lblDepartment.setText(workorder_department.name)
    main_window.ui.workorder_entryform_lblDepartment.setProperty(
        "object", workorder_department
    )

    main_window.ui.workorder_entryform_lblPriorityLevel.setText(
        workorder_prioritylevel.name
    )
    main_window.ui.workorder_entryform_lblPriorityLevel.setProperty(
        "object", workorder_prioritylevel
    )

    main_window.ui.workorder_entryform_txtPurchaseOrderNumber.setText(
        entity.purchase_order_number
    )

    main_window.ui.workorder_entryform_txtTaskDescription.setPlainText(
        entity.task_description
    )

    if comments := entity.comments:
        main_window.ui.workorder_entryform_txtComments.setPlainText(comments)

    date_allocated = entity.date_allocated
    main_window.ui.workorder_entryform_dteDateAllocated.setDate(
        QDate(date_allocated.year, date_allocated.month, date_allocated.day)
    )

    date_completed = entity.date_completed
    main_window.ui.workorder_entryform_chkIsComplete.setChecked(
        date_completed is not None
    )

    if date_completed:
        main_window.ui.workorder_entryform_dteDateCompleted.setDate(
            QDate(date_completed.year, date_completed.month, date_completed.day)
        )

        if close_out_comments := entity.close_out_comments:
            main_window.ui.workorder_entryform_txtCloseOutComments.setPlainText(
                close_out_comments
            )

    # TODO - Fill out unassigned and assigned items and assignee tables

    main_window.ui.workorder_entryform_txtPurchaseOrderNumber.setFocus()

    navigate(main_window, Page.WORKORDER_ENTRYFORM)


def delete_workorder(main_window) -> None:

    if not askyesno(
        "Confirm delete", "Are you sure you would like to delete the selected record?"
    ):
        return

    selected_id = selected_row_id(main_window.ui.workorder_listingview_tblWorkOrder)
    global global_workorders
    entity = global_workorders[selected_id]

    delete_entities_by_ids(WorkOrder, [entity.id])

    Notification(
        "Delete Successful", [f"Successfully deleted work order: {entity.id}"]
    ).show()

    load_workorder_listingview(main_window)


def workorder_entryform_is_valid(main_window) -> bool:

    error_strings = list()

    if not main_window.ui.workorder_entryform_lblSite.text():
        error_strings.append("A site must be selected.")

    if not main_window.ui.workorder_entryform_lblDepartment.text():
        error_strings.append("A department must be selected.")

    if not main_window.ui.workorder_entryform_lblPriorityLevel.text():
        error_strings.append("A priority level must be selected.")

    if not main_window.ui.workorder_entryform_tblAssignedItems.rowCount() >= 1:
        error_strings.append("At least one item must be assigned.")

    if not main_window.ui.workorder_entryform_txtTaskDescription.toPlainText():
        error_strings.append("Task Description field cannot be blank.")

    if not main_window.ui.workorder_entryform_tblAssignedAssignees.rowCount() >= 1:
        error_strings.append("At least one assignee must be assigned.")

    if error_strings:
        Notification("Cannot Save Work Order", error_strings).show()

    return not bool(error_strings)


def save_and_delete_workorderitems(main_window, entity_id):

    existing_item_ids = [
        woi.item_id
        for woi in select_by_attrs_dict(
            WorkOrderItem, {"workorder_id": entity_id}
        ).values()
    ]

    assigned_item_ids = list()
    workorderitems_to_save = list()

    tbl = main_window.ui.workorder_entryform_tblAssignedItems
    id_column_index = 0

    for row_index in tbl.rowCount():
        _cell = tbl.item(row_index, id_column_index)
        _id = int(_cell.text())
        assigned_item_ids.append(_id)

        if _id not in list(existing_item_ids.keys()):
            workorderitems_to_save.append(WorkOrderItem(None, entity_id, _id))

    for item_id in existing_item_ids:
        if item_id not in assigned_item_ids:
            delete_by_attrs_dict(
                WorkOrderItem, {"workorder_id": entity_id, "item_id": item_id}
            )

    save_by_list(workorderitems_to_save)


def save_and_delete_workorderassignees(main_window, entity_id):

    existing_assignee_ids = [
        woa.assignee_id
        for woa in select_by_attrs_dict(
            WorkOrderAssignee, {"workorder_id": entity_id}
        ).values()
    ]

    assigned_assignee_ids = list()
    workorderassignees_to_save = list()

    tbl = main_window.ui.workorder_entryform_tblAssignedAssignees
    id_column_index = 0

    for row_index in tbl.rowCount():
        _cell = tbl.item(row_index, id_column_index)
        _id = int(_cell.text())
        assigned_assignee_ids.append(_id)

        if _id not in list(existing_assignee_ids.keys()):
            workorderassignees_to_save.append(WorkOrderAssignee(None, entity_id, _id))

    for assignee_id in existing_assignee_ids:
        if assignee_id not in assigned_assignee_ids:
            delete_by_attrs_dict(
                WorkOrderAssignee,
                {"workorder_id": entity_id, "assignee_id": assignee_id},
            )

    save_by_list(workorderassignees_to_save)


def save_workorder(main_window) -> None:

    if not workorder_entryform_is_valid(main_window):
        return

    if not askyesno(
        "Confirm save", "Are you sure you would like to save the current record?"
    ):
        return

    entity_id = (
        None
        if len(main_window.ui.workorder_entryform_lblId.text()) == 0
        else int(main_window.ui.workorder_entryform_lblId.text())
    )
    date_created = (
        datetime.strptime(
            main_window.ui.workorder_entryform_lblDateCreated.text(), "%d-%m-%Y"
        ).date()
        if entity_id
        else date.today()
    )
    raisedby_user_id = (
        main_window.ui.workorder_entryform_lblRaisedBy.property("object").id
        if entity_id
        else main_window.current_user.id
    )
    selected_site = main_window.ui.workorder_entryform_lblSite.property("object")
    selected_department = main_window.ui.workorder_entryform_lblDepartment.property(
        "object"
    )
    selected_prioritylevel = (
        main_window.ui.workorder_entryform_lblPriorityLevel.property("object")
    )
    selected_date_allocated_qdate = (
        main_window.ui.workorder_entryform_dteDateAllocated.date()
    )
    selected_date_allocated = date(
        selected_date_allocated_qdate.year(),
        selected_date_allocated_qdate.month(),
        selected_date_allocated_qdate.day(),
    )
    selected_date_completed_qdate = (
        main_window.ui.workorder_entryform_dteDateCompleted.date()
    )
    selected_date_completed = (
        None
        if not main_window.ui.workorder_entryform_chkIsComplete.isChecked()
        else date(
            selected_date_completed_qdate.year(),
            selected_date_completed_qdate.month(),
            selected_date_completed_qdate.day(),
        )
    )
    close_out_comments = (
        None
        if not main_window.ui.workorder_entryform_chkIsComplete.isChecked()
        else main_window.ui.workorder_entryform_txtCloseOutComments.toPlainText()
    )

    entity = WorkOrder(
        entity_id,
        selected_site.id,
        selected_department.id,
        selected_prioritylevel.id,
        main_window.ui.workorder_entryform_txtTaskDescription.toPlainText(),
        main_window.ui.workorder_entryform_txtComments.toPlainText(),
        date_created,
        selected_date_allocated,
        raisedby_user_id,
        selected_date_completed,
        main_window.ui.workorder_entryform_txtPurchaseOrderNumber.text(),
        close_out_comments,
    )

    entity_id = sorted(save_by_list([entity]), key=lambda e: e.id, reverse=True)[0].id

    save_and_delete_workorderitems(main_window, entity_id)

    save_and_delete_workorderassignees(main_window, entity_id)

    Notification(
        "Safe Successful", [f"Successfully saved work order: {entity_id}"]
    ).show()

    load_workorder_listingview(main_window)

    clear_workorder_entryform(main_window)


def back_to_workorder_listingview(main_window) -> None:

    clear_workorder_entryform(main_window)

    navigate(main_window, Page.WORKORDER_LISTINGVIEW)


def workorders_by_search(main_window, search_text: str) -> None:

    global workorder_table_data

    if not search_text:
        matches = workorder_table_data
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
                        tup[6],
                        tup[11],
                    ]
                ).lower(),
                workorder_table_data,
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
            "Items": (5, None),
            "Assignees": (6, None),
            "Comments": (7, None),
            "Date Allocated": (8, None),
            "Date Completed": (9, None),
            "Close Out Comments": (10, None),
            "Raised By": (11, None),
            "Date Created": (12, None),
        },
    )


def set_workorder_button_visibility(main_window):

    if main_window.current_user.permission_level <= 1:
        set_button_visibility(
            [
                main_window.ui.workorder_listingview_btnNew,
                main_window.ui.workorder_listingview_btnEdit,
                main_window.ui.workorder_listingview_btnDelete,
            ],
            is_visible=False,
        )
    else:
        set_button_visibility(
            [main_window.ui.workorder_listingview_btnNew], is_visible=True
        )
        set_button_visibility(
            [
                main_window.ui.workorder_listingview_btnEdit,
                main_window.ui.workorder_listingview_btnDelete,
            ],
            is_visible=selected_row_id(
                main_window.ui.workorder_listingview_tblWorkOrder
            )
            is not None,
        )


def assign_item_to_workorder(main_window):

    unassigned_tbl = main_window.ui.workorder_entryform_tblUnassignedItems
    selected_items = unassigned_tbl.selectedItems()

    if not selected_items:
        return

    selected_row = selected_items[0].row()
    selected_id = int(selected_items[0].text())

    global global_items
    selected_entity = global_items[selected_id]

    unassigned_tbl.removeRow(selected_row)

    assigned_tbl = main_window.ui.workorder_entryform_tblAssignedItems
    new_last_row_index = assigned_tbl.rowCount()
    assigned_tbl.setRowCount(new_last_row_index + 1)

    assigned_tbl.setItem(
        new_last_row_index, 0, QTableWidgetItem(str(selected_entity.id))
    )
    assigned_tbl.setItem(new_last_row_index, 1, QTableWidgetItem(selected_entity.name))


def unassign_item_from_workorder(main_window):

    assigned_tbl = main_window.ui.workorder_entryform_tblAssignedItems
    selected_items = assigned_tbl.selectedItems()

    if not selected_items:
        return

    selected_row = selected_items[0].row()
    selected_id = int(selected_items[0].text())

    global global_items
    selected_entity = global_items[selected_id]

    assigned_tbl.removeRow(selected_row)

    unassigned_tbl = main_window.ui.workorder_entryform_tblUnassignedItems
    new_last_row_index = unassigned_tbl.rowCount()
    unassigned_tbl.setRowCount(new_last_row_index + 1)

    unassigned_tbl.setItem(
        new_last_row_index, 0, QTableWidgetItem(str(selected_entity.id))
    )
    unassigned_tbl.setItem(
        new_last_row_index, 1, QTableWidgetItem(selected_entity.name)
    )


def assign_assignee_to_workorder(main_window):

    unassigned_tbl = main_window.ui.workorder_entryform_tblUnassignedAssignees
    selected_items = unassigned_tbl.selectedItems()

    if not selected_items:
        return

    selected_row = selected_items[0].row()
    selected_id = int(selected_items[0].text())

    global global_assignees
    selected_entity = global_assignees[selected_id]

    unassigned_tbl.removeRow(selected_row)

    assigned_tbl = main_window.ui.workorder_entryform_tblAssignedAssignees
    new_last_row_index = assigned_tbl.rowCount()
    assigned_tbl.setRowCount(new_last_row_index + 1)

    assigned_tbl.setItem(
        new_last_row_index, 0, QTableWidgetItem(str(selected_entity.id))
    )
    assigned_tbl.setItem(new_last_row_index, 1, QTableWidgetItem(selected_entity.name))


def unassign_assignee_from_workorder(main_window):

    assigned_tbl = main_window.ui.workorder_entryform_tblAssignedAssignees
    selected_items = assigned_tbl.selectedItems()

    if not selected_items:
        return

    selected_row = selected_items[0].row()
    selected_id = int(selected_items[0].text())

    global global_assignees
    selected_entity = global_assignees[selected_id]

    assigned_tbl.removeRow(selected_row)

    unassigned_tbl = main_window.ui.workorder_entryform_tblUnassignedAssignees
    new_last_row_index = unassigned_tbl.rowCount()
    unassigned_tbl.setRowCount(new_last_row_index + 1)

    unassigned_tbl.setItem(
        new_last_row_index, 0, QTableWidgetItem(str(selected_entity.id))
    )
    unassigned_tbl.setItem(
        new_last_row_index, 1, QTableWidgetItem(selected_entity.name)
    )


def select_site(main_window):

    global global_sites
    global_sites = select_by_attrs_dict(Site)

    SelectWindow(
        global_sites,
        main_window.ui.workorder_entryform_lblSite.setText,
        "name",
        main_window.ui.workorder_entryform_lblSite.setProperty,
        {"id": "ID", "name": "Name"},
    )


def select_department(main_window):

    global global_departments
    global_departments = main_window.current_user.get_departments()

    SelectWindow(
        global_departments,
        main_window.ui.workorder_entryform_lblDepartment.setText,
        "name",
        main_window.ui.workorder_entryform_lblDepartment.setProperty,
        {"id": "ID", "name": "Name"},
    )


def select_prioritylevel(main_window):

    global global_prioritylevels
    global_prioritylevels = select_by_attrs_dict(PriorityLevel)

    SelectWindow(
        global_prioritylevels,
        main_window.ui.workorder_entryform_lblPriorityLevel.setText,
        "name",
        main_window.ui.workorder_entryform_lblPriorityLevel.setProperty,
        {"id": "ID", "name": "Name", "days_until_overdue": "Days Until Overdue"},
    )


def toggle_completed_section(main_window):

    is_completed = main_window.ui.workorder_entryform_chkIsComplete.isChecked()
    main_window.ui.workorder_entryform_dteDateCompleted.setEnabled(is_completed)
    main_window.ui.workorder_entryform_txtCloseOutComments.setEnabled(is_completed)


def load_selection_tables(main_window):

    department = main_window.ui.workorder_entryform_lblDepartment.property("object")

    if not department:
        main_window.ui.workorder_entryform_tblUnassignedItems.clear()
        main_window.ui.workorder_entryform_tblAssignedItems.clear()
        main_window.ui.workorder_entryform_tblUnassignedAssignees.clear()
        main_window.ui.workorder_entryform_tblAssignedAssignees.clear()
        return

    # TODO - load selection tables


def connect_workorder_actions(main_window) -> None:

    main_window.ui.action_workorders.triggered.connect(
        lambda: load_workorder_listingview(main_window)
    )
    main_window.ui.workorder_listingview_btnNew.clicked.connect(
        lambda: new_workorder(main_window)
    )
    main_window.ui.workorder_listingview_btnEdit.clicked.connect(
        lambda: edit_workorder(main_window)
    )
    main_window.ui.workorder_listingview_btnDelete.clicked.connect(
        lambda: delete_workorder(main_window)
    )
    main_window.ui.workorder_entryform_btnSave.clicked.connect(
        lambda: save_workorder(main_window)
    )
    main_window.ui.workorder_entryform_btnBack.clicked.connect(
        lambda: back_to_workorder_listingview(main_window)
    )
    main_window.ui.workorder_entryform_btnSelectSite.clicked.connect(
        lambda: select_site(main_window)
    )
    main_window.ui.workorder_entryform_btnSelectDepartment.clicked.connect(
        lambda: select_department(main_window)
    )
    main_window.ui.workorder_entryform_btnSelectPriorityLevel.clicked.connect(
        lambda: select_prioritylevel(main_window)
    )
    main_window.ui.workorder_entryform_btnAssignItemToWorkOrder.clicked.connect(
        lambda: assign_item_to_workorder(main_window)
    )
    main_window.ui.workorder_entryform_btnUnassignItemFromWorkOrder.clicked.connect(
        lambda: unassign_item_from_workorder(main_window)
    )
    main_window.ui.workorder_entryform_btnAssignAssigneeToWorkOrder.clicked.connect(
        lambda: assign_assignee_to_workorder(main_window)
    )
    main_window.ui.workorder_entryform_btnUnassignAssigneeFromWorkOrder.clicked.connect(
        lambda: unassign_assignee_from_workorder(main_window)
    )

    main_window.ui.workorder_listingview_txtSearch.textChanged.connect(
        lambda: workorders_by_search(
            main_window, main_window.ui.workorder_listingview_txtSearch.text().lower()
        )
    )
    main_window.ui.workorder_listingview_tblWorkOrder.itemSelectionChanged.connect(
        lambda: set_workorder_button_visibility(main_window)
    )
    main_window.ui.workorder_entryform_chkIsComplete.stateChanged.connect(
        lambda: toggle_completed_section(main_window)
    )
    main_window.ui.workorder_entryform_lblDepartment.textChanged.connect(
        lambda: load_selection_tables(main_window)
    )
