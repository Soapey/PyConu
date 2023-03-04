from tkinter.messagebox import askyesno
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import Qt

from conu.classes.Assignee import Assignee
from conu.classes.Department import Department
from conu.classes.AssigneeDepartment import AssigneeDepartment

from conu.db.SQLiteConnection import (
    delete_by_attrs_dict,
    get_by_user_departments,
    select_by_attrs_dict,
    save_by_list,
)
from conu.helpers import (
    load_entities_into_table,
    navigate,
    selected_row_id,
    create_notification,
    set_button_visibility,
)
from conu.ui.PageEnum import Page


assigned_department_ids = set()


def load_assignee_listingview(main_window) -> None:
    """Load the assignee listing view.

    This function retrieves a list of assignees based on the user's departments, and then displays the
    assignee listing view in the main window. The list of assignees is stored in the global_assignees
    variable for use in other parts of the application.

    Args:
        main_window: The main window object.

    Returns:
        None
    """

    global global_assignees
    global_assignees = get_by_user_departments(Assignee, main_window.current_user.id)

    main_window.ui.assignee_listingview_txtSearch.clear()

    assignees_by_search(main_window, None)

    navigate(main_window, Page.ASSIGNEE_LISTINGVIEW)


def clear_assignee_entryform(main_window, assignee_id: int = None) -> None:
    """Clear the assignee entry form.

    This function clears the assignee ID, name, and description fields in the assignee entry form of the
    main window.

    Args:
        main_window: The main window object.
        assignee_id: The ID of the assignee to check for assigned departments.

    Returns:
        None
    """

    main_window.ui.assignee_entryform_lblId.clear()  # Clear assignee ID label
    main_window.ui.assignee_entryform_txtName.clear()  # Clear assignee name text field
    main_window.ui.assignee_entryform_txtDescription.clear()  # Clear assignee description text field

    vbox_departments = (
        main_window.ui.assignee_entryform_vboxDepartments
    )  # Get assignee departments vertical box layout
    vbox_departments.setAlignment(Qt.AlignTop)
    while vbox_departments.count():
        widget_to_remove = vbox_departments.takeAt(0).widget()
        widget_to_remove.deleteLater()

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

    # Loop through each department and create a QCheckBox widget for it
    for department in list(global_departments.values()):
        checkbox = QCheckBox(
            department.name, main_window.ui.page_assignee_entryform
        )  # Create a QCheckBox widget with the department name and add it to the vbox_departments layout
        checkbox.setProperty("object", department)
        checkbox.setChecked(False)  # Set the checkbox to unchecked by default

        # Check if the department is assigned to the assignee, and if so, set the checkbox to checked
        if department.id in assigned_department_ids:
            checkbox.setChecked(True)

        vbox_departments.addWidget(
            checkbox
        )  # Add the checkbox widget to the vbox_departments layout


def new_assignee(main_window) -> None:
    """
    Create a new assignee record.

    This function clears the assignee entry form, sets focus on the name field, and navigates to the assignee
    entry form page.

    Args:
        main_window: The main window object.

    Returns:
        None
    """

    clear_assignee_entryform(main_window)
    main_window.ui.assignee_entryform_txtName.setFocus()
    navigate(main_window, Page.ASSIGNEE_ENTRYFORM)


def edit_assignee(main_window) -> None:
    """
    Edit an existing assignee record.

    This function retrieves the selected assignee record from the assignee listing view and populates the
    assignee entry form with its values. It then sets focus on the name field and navigates to the assignee
    entry form page.

    Args:
        main_window: The main window object.

    Returns:
        None
    """

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
    """
    Delete an assignee record.

    This function prompts the user to confirm deletion of the selected assignee record. If the user confirms,
    the function retrieves the selected assignee record from the assignee listing view and deletes it from the
    database. It then loads the assignee listing view page.

    Args:
        main_window: The main window object.

    Returns:
        None
    """

    if not askyesno(
        "Confirm delete", "Are you sure you would like to delete the selected record?"
    ):
        return
    selected_id = selected_row_id(main_window.ui.assignee_listingview_tblAssignee)
    global global_assignees
    entity = global_assignees[selected_id]
    delete_by_attrs_dict(Assignee, {"id": entity.id})
    create_notification(
        "Delete Successful",
        [f"Successfully deleted assignee: {entity.name}"],
        "#74c69d",
    )
    load_assignee_listingview(main_window)


def assignee_entryform_is_valid(main_window) -> bool:

    error_strings = list()

    entered_name = main_window.ui.assignee_entryform_txtName.text()

    if not entered_name:
        error_strings.append("Name field cannot be blank.")

    if error_strings:
        create_notification("Cannot Save Assignee", error_strings, "red")
        return False

    return True


def save_assignee(main_window) -> None:
    """
    Saves the current record to the database.

    If the user cancels the save operation, the function will exit without saving.

    Args:
        main_window: The instance of the main window.

    Returns:
        None
    """

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

    assigneedepartments_to_save = list()
    vbox_departments = main_window.ui.assignee_entryform_vboxDepartments
    for i in range(vbox_departments.count()):
        widget: QCheckBox = vbox_departments.itemAt(i).widget()
        department: Department = widget.property("object")

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

    create_notification(
        "Safe Successful", [f"Successfully saved assignee: {entity.name}"], "#74c69d"
    )

    load_assignee_listingview(main_window)

    clear_assignee_entryform(main_window)


def back_to_assignee_listingview(main_window) -> None:
    """
    Navigates back to the assignee listing view.

    Args:
        main_window: The instance of the main window.

    Returns:
        None
    """

    clear_assignee_entryform(main_window)

    navigate(main_window, Page.ASSIGNEE_LISTINGVIEW)


def assignees_by_search(main_window, search_text: str) -> None:
    """
    Filters the list of assignees by the given search text and loads the filtered
    assignees into the table in the assignee listing view.

    Args:
        main_window: The instance of the main window.
        search_text: The text to search for.

    Returns:
        None
    """

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

    is_visible = (
        selected_row_id(main_window.ui.assignee_listingview_tblAssignee) is None
    )

    set_button_visibility(
        [
            main_window.ui.assignee_listingview_btnEdit,
            main_window.ui.assignee_listingview_btnDelete,
        ],
        is_visible,
    )


def connect_assignee_actions(main_window) -> None:
    """
    Connects the actions for the assignee listing view and the assignee entry form.

    Args:
        main_window: The instance of the main window.

    Returns:
        None
    """

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
    main_window.ui.assignee_listingview_tblAssignee.currentItemChanged.connect(
        lambda: set_assignee_button_visibility(main_window)
    )
