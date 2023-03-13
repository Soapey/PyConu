from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox
from tkinter.messagebox import askyesno

from conu.classes.WorkOrder import WorkOrder
from conu.classes.UserDepartment import UserDepartment
from conu.classes.WorkOrderAssignee import WorkOrderAssignee
from conu.classes.WorkOrderItem import WorkOrderItem
from conu.classes.Department import Department
from conu.db.SQLiteConnection import (
    delete_by_attrs_dict,
    save_by_list,
    select_by_attrs_dict,
)
from conu.helpers import (
    clear_widget_children,
    navigate,
    selected_row_id,
    set_button_visibility,
    load_query_rows_into_table,
)
from conu.ui.components.Notification import Notification
from conu.ui.PageEnum import Page


def load_workorder_listingview(main_window) -> None:

    global global_workorders
    global workorder_table_data

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


def clear_workorder_entryform(main_window, workorder_id: int = None) -> None:

    # TODO - Clear WorkOrder entry form

    pass


def new_workorder(main_window) -> None:

    clear_workorder_entryform(main_window)

    main_window.ui.workorder_entryform_txtPurchaseOrderNumber.setFocus()

    navigate(main_window, Page.WORKORDER_ENTRYFORM)


def edit_workorder(main_window) -> None:

    selected_id = selected_row_id(main_window.ui.workorder_listingview_tblWorkOrder)
    global global_workorders
    entity = global_workorders[selected_id]

    clear_workorder_entryform(main_window, selected_id)

    # TODO - CLEAR FIELDS

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

    delete_by_attrs_dict(WorkOrder, {"id": entity.id})

    Notification(
        "Delete Successful", [f"Successfully deleted work order: {entity.id}"]
    ).show()

    load_workorder_listingview(main_window)


def workorder_entryform_is_valid(main_window) -> bool:

    error_strings = list()

    # TODO - Work Order entry form validation

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
