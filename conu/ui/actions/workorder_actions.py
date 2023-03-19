from PyQt5.QtCore import QDate
from tkinter.messagebox import askyesno
from datetime import datetime, date

from conu.classes.WorkOrder import WorkOrder
from conu.classes.UserDepartment import UserDepartment
from conu.classes.WorkOrderAssignee import WorkOrderAssignee
from conu.classes.WorkOrderItem import WorkOrderItem
from conu.classes.Department import Department
from conu.classes.Site import Site
from conu.classes.ItemDepartment import ItemDepartment
from conu.classes.AssigneeDepartment import AssigneeDepartment
from conu.classes.RecurringWorkOrderItem import RecurringWorkOrderItem
from conu.classes.PriorityLevel import PriorityLevel
from conu.classes.RecurringWorkOrder import RecurringWorkOrder
from conu.classes.ServiceTracker import ServiceTracker

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

recurringworkorder_id: int = None
servicetracker_id: int = None
unassigned_items_tbl: TableManager = None
assigned_items_tbl: TableManager = None
unassigned_assignees_tbl: TableManager = None
assigned_assignees_tbl: TableManager = None


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

    global_workorders = {
        wo.id: wo
        for wo in WorkOrder.get().values()
        if wo.department_id in user_department_ids
    }

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

    todays_date = date.today()

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

    main_window.ui.workorder_entryform_dteDateAllocated.setDate(
        QDate(todays_date.year, todays_date.month, todays_date.day)
    )
    main_window.ui.workorder_entryform_chkIsComplete.setChecked(False)

    main_window.ui.workorder_entryform_dteDateCompleted.setDate(
        QDate(todays_date.year, todays_date.month, todays_date.day)
    )
    main_window.ui.workorder_entryform_dteDateCompleted.setEnabled(False)

    main_window.ui.workorder_entryform_txtCloseOutComments.clear()
    main_window.ui.workorder_entryform_txtCloseOutComments.setEnabled(False)

    main_window.ui.workorder_entryform_lblCurrentUnits.setVisible(False)
    main_window.ui.workorder_entryform_spnCurrentUnits.setValue(1)
    main_window.ui.workorder_entryform_spnCurrentUnits.setVisible(False)

    main_window.ui.workorder_entryform_lblCalibrationDate.setVisible(False)
    main_window.ui.workorder_entryform_dteCalibrationDate.setDate(
        QDate(todays_date.year, todays_date.month, todays_date.day)
    )
    main_window.ui.workorder_entryform_dteCalibrationDate.setVisible(False)

    global unassigned_items_tbl, assigned_items_tbl, unassigned_assignees_tbl, assigned_assignees_tbl

    unassigned_items_tbl = TableManager(
        main_window.ui.workorder_entryform_tblUnassignedItems, ["ID", "Name"]
    )
    assigned_items_tbl = TableManager(
        main_window.ui.workorder_entryform_tblAssignedItems, ["ID", "Name"]
    )
    unassigned_assignees_tbl = TableManager(
        main_window.ui.workorder_entryform_tblUnassignedAssignees, ["ID", "Name"]
    )
    assigned_assignees_tbl = TableManager(
        main_window.ui.workorder_entryform_tblAssignedAssignees, ["ID", "Name"]
    )

    unassigned_items_tbl.clear()
    assigned_items_tbl.clear()
    unassigned_assignees_tbl.clear()
    assigned_assignees_tbl.clear()


def new_workorder(main_window) -> None:

    global recurringworkorder_id, servicetracker_id
    recurringworkorder_id = None
    servicetracker_id = None

    clear_workorder_entryform(main_window)

    load_selection_tables(main_window)

    main_window.ui.workorder_entryform_txtPurchaseOrderNumber.setFocus()

    navigate(main_window, Page.WORKORDER_ENTRYFORM)


def edit_workorder(
    main_window, entity=None, _recurringworkorder_id=None, _servicetracker_id=None
) -> None:

    global recurringworkorder_id, servicetracker_id
    recurringworkorder_id = _recurringworkorder_id
    servicetracker_id = _servicetracker_id

    users = select_by_attrs_dict(User)
    sites = select_by_attrs_dict(Site)
    departments = select_by_attrs_dict(Department)
    prioritylevels = select_by_attrs_dict(PriorityLevel)

    if not entity:
        workorders = WorkOrder.get()
        entity_id = selected_row_id(main_window.ui.workorder_listingview_tblWorkOrder)
        entity = workorders[entity_id]

    workorder_raisedby_user = None
    if entity.raisedby_user_id:
        workorder_raisedby_user = users[entity.raisedby_user_id]

    clear_workorder_entryform(main_window)

    if entity.id:
        main_window.ui.workorder_entryform_lblId.setText(str(entity.id))

    if entity.date_created:
        main_window.ui.workorder_entryform_lblDateCreated.setText(
            datetime.strftime(entity.date_created, "%d-%m-%Y")
        )

    if entity.raisedby_user_id:
        main_window.ui.workorder_entryform_lblRaisedBy.setText(
            f"{workorder_raisedby_user.first_name} {workorder_raisedby_user.last_name}"
        )
        main_window.ui.workorder_entryform_lblRaisedBy.setProperty(
            "object", workorder_raisedby_user
        )
    if entity.site_id:
        workorder_site = sites[entity.site_id]
        main_window.ui.workorder_entryform_lblSite.setProperty("object", workorder_site)
        main_window.ui.workorder_entryform_lblSite.setText(workorder_site.name)

    if entity.department_id:
        workorder_department = departments[entity.department_id]
        main_window.ui.workorder_entryform_lblDepartment.setProperty(
            "object", workorder_department
        )
        main_window.ui.workorder_entryform_lblDepartment.setText(
            workorder_department.name
        )

    if entity.prioritylevel_id:
        workorder_prioritylevel = prioritylevels[entity.prioritylevel_id]
        main_window.ui.workorder_entryform_lblPriorityLevel.setText(
            workorder_prioritylevel.name
        )
        main_window.ui.workorder_entryform_lblPriorityLevel.setProperty(
            "object", workorder_prioritylevel
        )

    if entity.purchase_order_number:
        main_window.ui.workorder_entryform_txtPurchaseOrderNumber.setText(
            entity.purchase_order_number
        )

    main_window.ui.workorder_entryform_txtTaskDescription.setPlainText(
        entity.task_description
    )

    if comments := entity.comments:
        main_window.ui.workorder_entryform_txtComments.setPlainText(comments)

    if entity.date_allocated:
        date_allocated = entity.date_allocated
        main_window.ui.workorder_entryform_dteDateAllocated.setDate(
            QDate(date_allocated.year, date_allocated.month, date_allocated.day)
        )

    if entity.date_completed:

        date_completed = entity.date_completed

        main_window.ui.workorder_entryform_chkIsComplete.setChecked(
            date_completed is not None
        )

        main_window.ui.workorder_entryform_dteDateCompleted.setDate(
            QDate(date_completed.year, date_completed.month, date_completed.day)
        )

        if close_out_comments := entity.close_out_comments:
            main_window.ui.workorder_entryform_txtCloseOutComments.setPlainText(
                close_out_comments
            )

    if servicetracker_id:
        servicetrackers = ServiceTracker.get()
        servicetracker = servicetrackers[servicetracker_id]

        calibration_date = servicetracker.units_calibration_date
        main_window.ui.workorder_entryform_lblCalibrationDate.setVisible(True)
        main_window.ui.workorder_entryform_dteCalibrationDate.setVisible(True)
        main_window.ui.workorder_entryform_dteCalibrationDate.setDate(
            QDate(
                calibration_date.year,
                calibration_date.month,
                calibration_date.day,
            )
        )

        main_window.ui.workorder_entryform_lblCurrentUnits.setVisible(True)
        main_window.ui.workorder_entryform_spnCurrentUnits.setVisible(True)
        main_window.ui.workorder_entryform_spnCurrentUnits.setValue(
            servicetracker.current_units
        )

    load_selection_tables(main_window)

    main_window.ui.workorder_entryform_txtPurchaseOrderNumber.setFocus()

    navigate(main_window, Page.WORKORDER_ENTRYFORM)


def delete_workorder(main_window) -> None:

    if not askyesno(
        "Confirm delete", "Are you sure you would like to delete the selected record?"
    ):
        return

    selected_id = selected_row_id(main_window.ui.workorder_listingview_tblWorkOrder)

    workorders = select_by_attrs_dict(WorkOrder)
    entity = workorders[selected_id]

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

    for row_index in range(tbl.rowCount()):
        _cell = tbl.item(row_index, id_column_index)
        _id = int(_cell.text())
        assigned_item_ids.append(_id)

        if _id not in list(existing_item_ids):
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

    for row_index in range(tbl.rowCount()):
        _cell = tbl.item(row_index, id_column_index)
        _id = int(_cell.text())
        assigned_assignee_ids.append(_id)

        if _id not in list(existing_assignee_ids):
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

    recurringworkorder = None
    if recurringworkorder_id:
        recurringworkorders = RecurringWorkOrder.get()
        recurringworkorder = recurringworkorders[recurringworkorder_id]

        new_recurringworkorder = RecurringWorkOrder(
            recurringworkorder.id,
            recurringworkorder.site_id,
            recurringworkorder.department_id,
            recurringworkorder.prioritylevel_id,
            recurringworkorder.task_description,
            recurringworkorder.comments,
            recurringworkorder.type,
            recurringworkorder.start_date,
            date.today(),
            recurringworkorder.interval,
            recurringworkorder.weekdays,
            recurringworkorder.day,
            recurringworkorder.month,
            recurringworkorder.month_weekday_occurrence,
        )

        save_by_list([new_recurringworkorder])

    if servicetracker_id:
        servicetrackers = select_by_attrs_dict(ServiceTracker)
        servicetracker = servicetrackers[servicetracker_id]
        new_calibration_qdate = (
            main_window.ui.workorder_entryform_dteCalibrationDate.date()
        )
        new_calibrationdate = date(
            new_calibration_qdate.year(),
            new_calibration_qdate.month(),
            new_calibration_qdate.day(),
        )
        new_currentunits = main_window.ui.workorder_entryform_spnCurrentUnits.value()

        new_servicetracker = ServiceTracker(
            servicetracker.id,
            servicetracker.item_id,
            new_calibrationdate,
            new_currentunits,
            servicetracker.average_units_per_day,
            new_currentunits + servicetracker.service_interval,
            servicetracker.service_interval,
        )

        save_by_list([new_servicetracker])

    Notification(
        "Save Successful", [f"Successfully saved work order: {entity_id}"]
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
                        tup[6],
                        tup[7],
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
            "Comments": (5, None),
            "Items": (6, None),
            "Assignees": (7, None),
            "Date Allocated": (8, None),
            "Date Completed": (9, None),
            "Close Out Comments": (10, None),
            "Raised By": (11, None),
            "Date Created": (12, None),
        },
    )


def save_workorder_to_pdf(main_window):

    selected_id = selected_row_id(main_window.ui.workorder_listingview_tblWorkOrder)

    if not selected_id:
        return

    selected_entity = WorkOrder.get()[selected_id]

    selected_entity.save_to_pdf()


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
                main_window.ui.workorder_listingview_btnPDF,
            ],
            is_visible=selected_row_id(
                main_window.ui.workorder_listingview_tblWorkOrder
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


def transfer_assignee_to_table(from_table: TableManager, to_table: TableManager):

    selected_item = from_table.first_selected_item()

    if not selected_item:
        return

    selected_row = selected_item.row()
    selected_id = int(selected_item.text())

    assignees = select_by_attrs_dict(Assignee)
    selected_entity = assignees[selected_id]

    from_table.remove_row(selected_row)

    to_table.add_row()

    to_table.set_item(to_table.last_row_index, 0, str(selected_id))
    to_table.set_item(to_table.last_row_index, 1, selected_entity.name)


def select_site(main_window):

    sites = select_by_attrs_dict(Site)

    SelectWindow(
        sites,
        main_window.ui.workorder_entryform_lblSite.setText,
        "name",
        main_window.ui.workorder_entryform_lblSite.setProperty,
        {"id": "ID", "name": "Name"},
    )


def select_department(main_window):

    global servicetracker_id

    departments = dict()
    if servicetracker_id:
        servicetrackers = select_by_attrs_dict(ServiceTracker)
        servicetracker = servicetrackers[servicetracker_id]
        itemdepartments = select_by_attrs_dict(
            ItemDepartment, {"item_id": servicetracker.item_id}
        ).values()
        department_ids = {id.department_id for id in itemdepartments}
        all_departments = select_by_attrs_dict(Department).values()
        departments = {d.id: d for d in all_departments if d.id in department_ids}
    else:
        departments = main_window.current_user.get_departments()

    SelectWindow(
        departments,
        main_window.ui.workorder_entryform_lblDepartment.setText,
        "name",
        main_window.ui.workorder_entryform_lblDepartment.setProperty,
        {"id": "ID", "name": "Name"},
        lambda: load_selection_tables(main_window),
    )


def select_prioritylevel(main_window):

    prioritylevels = select_by_attrs_dict(PriorityLevel)

    SelectWindow(
        prioritylevels,
        main_window.ui.workorder_entryform_lblPriorityLevel.setText,
        "name",
        main_window.ui.workorder_entryform_lblPriorityLevel.setProperty,
        {"id": "ID", "name": "Name", "days_until_overdue": "Days Until Overdue"},
    )


def toggle_completed_section(main_window):

    is_completed = main_window.ui.workorder_entryform_chkIsComplete.isChecked()
    main_window.ui.workorder_entryform_dteDateCompleted.setEnabled(is_completed)
    main_window.ui.workorder_entryform_txtCloseOutComments.setEnabled(is_completed)


def load_item_selection_table(main_window):

    id = main_window.ui.workorder_entryform_lblId.text()

    department = main_window.ui.workorder_entryform_lblDepartment.property("object")

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

    if (
        (id is None or len(id) == 0)
        and not recurringworkorder_id
        and not servicetracker_id
    ):
        load_entities_into_table(
            unassigned_items_tbl.table, items, {"id": "ID", "name": "Name"}
        )
        return

    assigned_item_ids = None
    if recurringworkorder_id:
        assigned_item_ids = [
            rwoi.item_id
            for rwoi in select_by_attrs_dict(
                RecurringWorkOrderItem, {"recurringworkorder_id": recurringworkorder_id}
            ).values()
        ]
    elif servicetracker_id:
        servicetrackers = select_by_attrs_dict(ServiceTracker)
        servicetracker = servicetrackers[servicetracker_id]
        assigned_item_ids = [servicetracker.item_id]
    else:
        id = int(id)
        assigned_item_ids = [
            woi.item_id
            for woi in select_by_attrs_dict(
                WorkOrderItem, {"workorder_id": id}
            ).values()
        ]

    unassigned_items = [item for item in items if item.id not in assigned_item_ids]
    assigned_items = [all_items[item_id] for item_id in assigned_item_ids]

    load_entities_into_table(
        unassigned_items_tbl.table, unassigned_items, {"id": "ID", "name": "Name"}
    )
    load_entities_into_table(
        assigned_items_tbl.table, assigned_items, {"id": "ID", "name": "Name"}
    )


def load_assignee_selection_table(main_window):

    id = main_window.ui.workorder_entryform_lblId.text()

    department = main_window.ui.workorder_entryform_lblDepartment.property("object")

    global unassigned_assignees_tbl, assigned_assignees_tbl
    unassigned_assignees_tbl.clear()
    assigned_assignees_tbl.clear()

    if department is None:
        return

    all_assignees = select_by_attrs_dict(Assignee)

    assignee_departments = select_by_attrs_dict(
        AssigneeDepartment, {"department_id": department.id}
    ).values()
    assignees = [
        all_assignees[assignee_id]
        for assignee_id in {ad.assignee_id for ad in assignee_departments}
    ]
    assignees = sorted(assignees, key=lambda e: e.name)

    global recurringworkorder_id
    if id is None or len(id) == 0 or recurringworkorder_id or servicetracker_id:
        load_entities_into_table(
            unassigned_assignees_tbl.table, assignees, {"id": "ID", "name": "Name"}
        )
        return

    id = int(id)

    workorder_assignees = select_by_attrs_dict(WorkOrderAssignee, {"workorder_id": id})
    assigned_assignee_ids = [woa.assignee_id for woa in workorder_assignees.values()]
    assigned_assignees = [
        all_assignees[assignee_id] for assignee_id in assigned_assignee_ids
    ]
    unassigned_assignees = [
        assignee for assignee in assignees if assignee.id not in assigned_assignee_ids
    ]
    load_entities_into_table(
        unassigned_assignees_tbl.table,
        unassigned_assignees,
        {"id": "ID", "name": "Name"},
    )
    load_entities_into_table(
        assigned_assignees_tbl.table,
        assigned_assignees,
        {"id": "ID", "name": "Name"},
    )


def load_selection_tables(main_window):

    load_item_selection_table(main_window)

    load_assignee_selection_table(main_window)


def connect_workorder_actions(main_window) -> None:

    global unassigned_items_tbl, assigned_items_tbl, unassigned_assignees_tbl, assigned_assignees_tbl

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
        lambda: transfer_item_to_table(unassigned_items_tbl, assigned_items_tbl)
    )
    main_window.ui.workorder_entryform_btnUnassignItemFromWorkOrder.clicked.connect(
        lambda: transfer_item_to_table(assigned_items_tbl, unassigned_items_tbl)
    )
    main_window.ui.workorder_entryform_btnAssignAssigneeToWorkOrder.clicked.connect(
        lambda: transfer_assignee_to_table(
            unassigned_assignees_tbl, assigned_assignees_tbl
        )
    )
    main_window.ui.workorder_entryform_btnUnassignAssigneeFromWorkOrder.clicked.connect(
        lambda: transfer_assignee_to_table(
            assigned_assignees_tbl, unassigned_assignees_tbl
        )
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
    main_window.ui.workorder_listingview_btnPDF.clicked.connect(
        lambda: save_workorder_to_pdf(main_window)
    )
