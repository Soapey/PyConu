from tkinter.messagebox import askyesno

from conu.classes.Department import Department
from conu.db.SQLiteConnection import (
    delete_by_attrs_dict,
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


def load_department_listingview(main_window) -> None:
    """Load the department listing view for the given main window.

    This function sets the global `global_departments` variable to the departments
    associated with the current user. It also clears the search field and displays
    all departments. Finally, it navigates the main window to the department listing view.

    Args:
        main_window (MainWindow): The main window to load the department listing view for.

    Returns:
        None
    """

    global global_departments
    global_departments = select_by_attrs_dict(Department)

    main_window.ui.department_listingview_txtSearch.clear()

    departments_by_search(main_window, None)

    set_department_button_visibility(main_window)

    navigate(main_window, Page.DEPARTMENT_LISTINGVIEW)


def clear_department_entryform(main_window) -> None:
    """Clear the department entry form for the given main window.

    This function clears the ID and name fields of the department entry form.

    Args:
        main_window (MainWindow): The main window to clear the department entry form for.

    Returns:
        None
    """

    main_window.ui.department_entryform_lblId.clear()
    main_window.ui.department_entryform_txtName.clear()


def new_department(main_window) -> None:
    """Create a new department using the department entry form in the given main window.

    This function clears the department entry form and sets focus on the name field. It then
    navigates the main window to the department entry form.

    Args:
        main_window (MainWindow): The main window to create a new department for.

    Returns:
        None
    """

    clear_department_entryform(main_window)
    main_window.ui.department_entryform_txtName.setFocus()
    navigate(main_window, Page.DEPARTMENT_ENTRYFORM)


def edit_department(main_window) -> None:
    """Edit the selected department using the department entry form in the given main window.

    This function gets the ID of the selected department from the department listing view, and
    populates the ID and name fields of the department entry form with the department's current
    values. It then sets focus on the name field and navigates the main window to the department
    entry form.

    Args:
        main_window (MainWindow): The main window to edit the selected department for.

    Returns:
        None
    """

    selected_id = selected_row_id(main_window.ui.department_listingview_tblDepartment)
    global global_departments
    entity = global_departments[selected_id]
    main_window.ui.department_entryform_lblId.setText(str(entity.id))
    main_window.ui.department_entryform_txtName.setText(entity.name)
    main_window.ui.department_entryform_txtName.setFocus()
    navigate(main_window, Page.DEPARTMENT_ENTRYFORM)


def delete_department(main_window) -> None:
    """
    Deletes the selected record.

    Args:
        main_window (MainWindow): The main window.

    Returns:
        None.
    """
    if not askyesno(
        "Confirm delete", "Are you sure you would like to delete the selected record?"
    ):
        return
    selected_id = selected_row_id(main_window.ui.department_listingview_tblDepartment)
    global global_departments
    entity = global_departments[selected_id]
    delete_by_attrs_dict(Department, {"id": entity.id})
    create_notification(
        "Delete Successful",
        [f"Successfully deleted department: {entity.name}"],
        "#74c69d",
    )
    load_department_listingview(main_window)


def department_entryform_is_valid(main_window) -> bool:

    error_strings = list()

    entered_name = main_window.ui.department_entryform_txtName.text()

    if not entered_name:
        error_strings.append("Name field cannot be blank.")

    if error_strings:
        create_notification("Cannot Save Department", error_strings, "red")
        return False

    return True


def save_department(main_window) -> None:
    """
    Saves the current record.

    Args:
        main_window (MainWindow): The main window.

    Returns:
        None.
    """

    if not department_entryform_is_valid(main_window):
        return

    if not askyesno(
        "Confirm save", "Are you sure you would like to save the current record?"
    ):
        return

    entity = Department(
        None
        if len(main_window.ui.department_entryform_lblId.text()) == 0
        else int(main_window.ui.department_entryform_lblId.text()),
        main_window.ui.department_entryform_txtName.text(),
    )

    save_by_list([entity])

    create_notification(
        "Save Successful", [f"Successfully saved form: {entity.name}"], "#74c69d"
    )

    load_department_listingview(main_window)

    clear_department_entryform(main_window)


def back_to_department_listingview(main_window) -> None:
    """Clear the department entry form and navigate back to the department listing view page.

    Args:
        main_window (MainWindow): The main window instance.

    Returns:
        None.
    """
    clear_department_entryform(main_window)

    navigate(main_window, Page.DEPARTMENT_LISTINGVIEW)


def departments_by_search(main_window, search_text: str) -> None:
    """Search for departments that match the specified search text and load them into the table view.

    Args:
        main_window (MainWindow): The main window instance.
        search_text (str): The search text to use when searching for departments.

    Returns:
        None.
    """
    global global_departments

    if not search_text:
        matches = list(global_departments.values())
    else:
        matches = list(
            filter(
                lambda e: search_text in "".join([str(e.id), e.name.lower()]),
                global_departments.values(),
            )
        )

    load_entities_into_table(
        main_window.ui.department_listingview_tblDepartment,
        matches,
        {"id": "ID", "name": "Name"},
    )


def set_department_button_visibility(main_window):

    is_visible = (
        selected_row_id(main_window.ui.department_listingview_tblDepartment) is not None
    )

    set_button_visibility(
        [
            main_window.ui.department_listingview_btnEdit,
            main_window.ui.department_listingview_btnDelete,
        ],
        is_visible,
    )


def connect_department_actions(main_window) -> None:
    """Connect department-related actions in the main window to their corresponding functions.

    Args:
        main_window (MainWindow): The main window instance.

    Returns:
        None.
    """
    main_window.ui.department_listingview_btnNew.clicked.connect(
        lambda: new_department(main_window)
    )
    main_window.ui.department_listingview_btnEdit.clicked.connect(
        lambda: edit_department(main_window)
    )
    main_window.ui.department_listingview_btnDelete.clicked.connect(
        lambda: delete_department(main_window)
    )
    main_window.ui.department_entryform_btnSave.clicked.connect(
        lambda: save_department(main_window)
    )
    main_window.ui.department_entryform_btnBack.clicked.connect(
        lambda: back_to_department_listingview(main_window)
    )
    main_window.ui.department_listingview_txtSearch.textChanged.connect(
        lambda: departments_by_search(
            main_window, main_window.ui.department_listingview_txtSearch.text().lower()
        )
    )
    main_window.ui.department_listingview_tblDepartment.itemSelectionChanged.connect(
        lambda: set_department_button_visibility(main_window)
    )
