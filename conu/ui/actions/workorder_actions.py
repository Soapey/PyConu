from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox
from tkinter.messagebox import askyesno

from conu.classes.WorkOrder import WorkOrder
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
    load_entities_into_table,
    navigate,
    selected_row_id,
    set_button_visibility,
)
from conu.ui.components.Notification import Notification
from conu.ui.PageEnum import Page


assigned_department_ids = set()


def load_workorder_listingview(main_window) -> None:

    WorkOrder.load_listingview_table_contents(main_window)

    main_window.ui.workorder_listingview_txtSearch.clear()

    workorders_by_search(main_window, None)

    set_workorder_button_visibility(main_window)

    navigate(main_window, Page.WORKORDER_LISTINGVIEW)


def clear_assignee_entryform(main_window, assignee_id: int = None) -> None:

    main_window.ui.workorder_entryform_lblId.clear()
    main_window.ui.workorder_entryform_lblDateCreated.clear()
    main_window.ui.workorder_entryform_lblRaisedBy.clear()

    main_window.ui.workorder_entryform_lblSite.clear()
    main_window.ui.workorder_entryform_lblSite.setProperty("object", None)

    main_window.ui.workorder_entryform_lblDepartment.clear()
    main_window.ui.workorder_entryform_lblDepartment.setProperty("object", None)

    main_window.ui.workorder_entryform_lblPriorityLevel.clear()
    main_window.ui.workorder_entryform_lblPriorityLevel.setProperty("object", None)

    main_window.ui.workorder_entryform_txtPurchaseOrderNumber.clear()

    # Retrieve global_departments and global_assigneedepartments using select_by_attrs_dict function
    global global_departments
    global global_assigneedepartments
    global_departments = select_by_attrs_dict(Department)
    global_assigneedepartments = select_by_attrs_dict(AssigneeDepartment)

    # Create a set to store the IDs of departments assigned to the assignee, if an assignee ID has been provided
    global assigned_department_ids
    if assignee_id:
        assigned_department_ids = {
            ad.department_id
            for ad in global_assigneedepartments.values()
            if ad.assignee_id == assignee_id
        }
    else:
        assigned_department_ids = set()

    # Loop through each department and create a QCheckBox widget for it
    for department in list(global_departments.values()):

        # Create a QCheckBox widget with the department name and add it to the vbox_departments layout
        checkbox = QCheckBox(department.name, main_window.ui.page_assignee_entryform)
        checkbox.setProperty("object", department)
        checkbox.setChecked(False)  # Set the checkbox to unchecked by default

        # Check if the department is assigned to the assignee, and if so, set the checkbox to checked
        if department.id in assigned_department_ids:
            checkbox.setChecked(True)

        # Add the checkbox widget to the vbox_departments layout
        vboxDepartments.addWidget(checkbox)


def new_assignee(main_window) -> None:

    clear_assignee_entryform(main_window)

    main_window.ui.assignee_entryform_txtName.setFocus()

    navigate(main_window, Page.ASSIGNEE_ENTRYFORM)


def edit_assignee(main_window) -> None:

    selected_id = selected_row_id(main_window.ui.assignee_listingview_tblAssignee)
    global global_assignees
    entity = global_assignees[selected_id]

    clear_assignee_entryform(main_window, selected_id)

    main_window.ui.assignee_entryform_lblId.setText(str(entity.id))
    main_window.ui.assignee_entryform_txtName.setText(entity.name)
    main_window.ui.assignee_entryform_txtDescription.setPlainText(entity.description)
    main_window.ui.assignee_entryform_txtName.setFocus()

    navigate(main_window, Page.ASSIGNEE_ENTRYFORM)


def delete_assignee(main_window) -> None:

    if not askyesno(
        "Confirm delete", "Are you sure you would like to delete the selected record?"
    ):
        return

    selected_id = selected_row_id(main_window.ui.assignee_listingview_tblAssignee)
    global global_assignees
    entity = global_assignees[selected_id]

    delete_by_attrs_dict(Assignee, {"id": entity.id})

    Notification(
        "Delete Successful", [f"Successfully deleted assignee: {entity.name}"]
    ).show()

    load_assignee_listingview(main_window)


def assignee_entryform_is_valid(main_window) -> bool:

    error_strings = list()

    if not main_window.ui.assignee_entryform_txtName.text():
        error_strings.append("Name field cannot be blank.")

    vboxDepartments = main_window.ui.assignee_entryform_vboxDepartments
    if not any(
        [
            vboxDepartments.itemAt(i).widget().isChecked()
            for i in range(vboxDepartments.count())
        ]
    ):
        error_strings.append("At least one department must be selected.")

    if error_strings:
        Notification("Cannot Save Assignee", error_strings).show()

    return not bool(error_strings)


def save_and_delete_assigneedepartments(main_window, entity_id):

    assigneedepartments_to_save = list()
    vboxDepartments = main_window.ui.assignee_entryform_vboxDepartments
    for i in range(vboxDepartments.count()):
        widget = vboxDepartments.itemAt(i).widget()
        if isinstance(widget, QCheckBox):
            department = widget.property("object")

            if widget.isChecked():

                if department.id not in assigned_department_ids:
                    assigneedepartments_to_save.append(
                        AssigneeDepartment(None, entity_id, department.id)
                    )

            else:

                if department.id in assigned_department_ids:
                    delete_by_attrs_dict(
                        AssigneeDepartment,
                        {"assignee_id": entity_id, "department_id": department.id},
                    )

    save_by_list(assigneedepartments_to_save)


def save_assignee(main_window) -> None:

    if not assignee_entryform_is_valid(main_window):
        return

    if not askyesno(
        "Confirm save", "Are you sure you would like to save the current record?"
    ):
        return

    entity = Assignee(
        None
        if len(main_window.ui.assignee_entryform_lblId.text()) == 0
        else int(main_window.ui.assignee_entryform_lblId.text()),
        main_window.ui.assignee_entryform_txtName.text(),
        main_window.ui.assignee_entryform_txtDescription.toPlainText(),
    )

    entity_id = sorted(save_by_list([entity]), key=lambda e: e.id, reverse=True)[0].id

    save_and_delete_assigneedepartments(main_window, entity_id)

    Notification(
        "Safe Successful", [f"Successfully saved assignee: {entity.name}"]
    ).show()

    load_assignee_listingview(main_window)

    clear_assignee_entryform(main_window)


def back_to_assignee_listingview(main_window) -> None:

    clear_assignee_entryform(main_window)

    navigate(main_window, Page.ASSIGNEE_LISTINGVIEW)


def assignees_by_search(main_window, search_text: str) -> None:

    global global_assignees

    if not search_text:
        matches = list(global_assignees.values())
    else:
        matches = list(
            filter(
                lambda e: search_text in "".join([str(e.id), e.name.lower()]),
                global_assignees.values(),
            )
        )

    load_entities_into_table(
        main_window.ui.assignee_listingview_tblAssignee,
        matches,
        {"id": "ID", "name": "Name", "description": "Description"},
    )


def set_assignee_button_visibility(main_window):

    if main_window.current_user.permission_level <= 1:
        set_button_visibility(
            [
                main_window.ui.assignee_listingview_btnNew,
                main_window.ui.assignee_listingview_btnEdit,
                main_window.ui.assignee_listingview_btnDelete,
            ],
            is_visible=False,
        )
    else:
        set_button_visibility(
            [main_window.ui.assignee_listingview_btnNew], is_visible=True
        )
        set_button_visibility(
            [
                main_window.ui.assignee_listingview_btnEdit,
                main_window.ui.assignee_listingview_btnDelete,
            ],
            is_visible=selected_row_id(main_window.ui.assignee_listingview_tblAssignee)
            is not None,
        )


def connect_workorder_actions(main_window) -> None:

    main_window.ui.assignee_listingview_btnNew.clicked.connect(
        lambda: new_assignee(main_window)
    )
    main_window.ui.assignee_listingview_btnEdit.clicked.connect(
        lambda: edit_assignee(main_window)
    )
    main_window.ui.assignee_listingview_btnDelete.clicked.connect(
        lambda: delete_assignee(main_window)
    )
    main_window.ui.assignee_entryform_btnSave.clicked.connect(
        lambda: save_assignee(main_window)
    )
    main_window.ui.assignee_entryform_btnBack.clicked.connect(
        lambda: back_to_assignee_listingview(main_window)
    )
    main_window.ui.assignee_listingview_txtSearch.textChanged.connect(
        lambda: assignees_by_search(
            main_window, main_window.ui.assignee_listingview_txtSearch.text().lower()
        )
    )
    main_window.ui.assignee_listingview_tblAssignee.itemSelectionChanged.connect(
        lambda: set_assignee_button_visibility(main_window)
    )
