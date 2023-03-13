from PyQt5.QtCore import QDate
from tkinter.messagebox import askyesno
from datetime import datetime

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
    save_by_list,
    select_by_attrs_dict,
    get_by_user_departments,
)
from conu.helpers import (
    clear_widget_children,
    navigate,
    selected_row_id,
    set_button_visibility,
    load_query_rows_into_table,
    load_entities_into_table,
)
from conu.ui.components.Notification import Notification
from conu.ui.PageEnum import Page


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

    load_entities_into_table(
        main_window.ui.workorder_entryform_tblUnassignedItems,
        global_items,
        {"id": "ID", "name": "Name"},
    )
    main_window.ui.workorder_entryform_tblAssignedItems.clear()

    load_entities_into_table(
        main_window.ui.workorder_entryform_tblUnassignedAssignees,
        global_assignees,
        {"id": "ID", "name": "Name"},
    )
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

    main_window.ui.workorder_entryform_txtPurchaseOrderNumber.setFocus()

    workorderitem_itemids = [
        woi.item_id
        for woi in select_by_attrs_dict(
            WorkOrderItem, {"workorder_id", entity.id}
        ).values()
    ]
    assigned_items = {
        item.id: item for item in global_items if item.id in workorderitem_itemids
    }
    load_entities_into_table(
        main_window.ui.workorder_entryform_tblUnassignedItems,
        dict(filter(lambda _, item: item not in assigned_items.values(), global_items)),
        {"id": "ID", "name": "Name"},
    )
    load_entities_into_table(
        main_window.ui.workorder_entryform_tblAssignedItems,
        assigned_items,
        {"id": "ID", "name": "Name"},
    )

    workorderassignee_assigneeids = [
        woa.assignee_id
        for woa in select_by_attrs_dict(
            WorkOrderAssignee, {"workorder_id", entity.id}
        ).values()
    ]
    assigned_assignees = {
        assignee.id: assignee
        for assignee in global_assignees
        if assignee.id in workorderassignee_assigneeids
    }
    load_entities_into_table(
        main_window.ui.workorder_entryform_tblUnassignedAssignees,
        dict(
            filter(
                lambda _, assignee: assignee not in assigned_assignees.values(),
                global_assignees,
            )
        ),
        {"id": "ID", "name": "Name"},
    )
    load_entities_into_table(
        main_window.ui.workorder_entryform_tblAssignedAssignees,
        assigned_assignees,
        {"id": "ID", "name": "Name"},
    )

    navigate(main_window, Page.WORKORDER_ENTRYFORM)


def delete_workorder(main_window) -> None:

    if not askyesno(
        "Confirm delete", "Are you sure you would like to delete the selected record?"
    ):
        return

    selected_id = selected_row_id(main_window.ui.workorder_listingview_tblWorkOrder)
    global global_workorders
    entity = global_workorders[selected_id]

    delete_by_attrs_dict(WorkOrder, {"id": entity.id})

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

    # TODO - Save and Delete attached WorkOrder items

    # assigneedepartments_to_save = list()
    # vboxDepartments = main_window.ui.assignee_entryform_vboxDepartments
    # for i in range(vboxDepartments.count()):
    #     widget = vboxDepartments.itemAt(i).widget()
    #     if isinstance(widget, QCheckBox):
    #         department = widget.property("object")

    #         if widget.isChecked():

    #             if department.id not in assigned_department_ids:
    #                 assigneedepartments_to_save.append(
    #                     AssigneeDepartment(None, entity_id, department.id)
    #                 )

    #         else:

    #             if department.id in assigned_department_ids:
    #                 delete_by_attrs_dict(
    #                     AssigneeDepartment,
    #                     {"assignee_id": entity_id, "department_id": department.id},
    #                 )

    # save_by_list(assigneedepartments_to_save)

    pass


def save_and_delete_workorderassignees(main_window, entity_id):

    # TODO - Save and Delete attached WorkOrder assignees

    pass


def save_workorder(main_window) -> None:

    if not workorder_entryform_is_valid(main_window):
        return

    if not askyesno(
        "Confirm save", "Are you sure you would like to save the current record?"
    ):
        return

    entity = WorkOrder(
        None
        if len(main_window.ui.workorder_entryform_lblId.text()) == 0
        else int(main_window.ui.workorder_entryform_lblId.text()),
        main_window.ui.workorder_entryform_txtName.text(),
        main_window.ui.workorder_entryform_txtDescription.toPlainText(),
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
    main_window.ui.workorder_listingview_txtSearch.textChanged.connect(
        lambda: workorders_by_search(
            main_window, main_window.ui.workorder_listingview_txtSearch.text().lower()
        )
    )
    main_window.ui.workorder_listingview_tblWorkOrder.itemSelectionChanged.connect(
        lambda: set_workorder_button_visibility(main_window)
    )
