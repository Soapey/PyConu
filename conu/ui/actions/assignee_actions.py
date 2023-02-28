from tkinter.messagebox import askyesno

from conu.classes.Assignee import Assignee
from conu.db.SQLiteConnection import (
    delete_by_attrs_dict,
    get_by_user_departments,
    save_by_list,
)
from conu.helpers import (
    load_entities_into_table,
    navigate,
    selected_row_id,
)
from conu.ui.PageEnum import Page
from conu.ui.components.MainWindow import MainWindow


def load_assignee_listingview(main_window: MainWindow) -> None:
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


def clear_assignee_entryform(main_window: MainWindow) -> None:
    """Clear the assignee entry form.

    This function clears the assignee ID, name, and description fields in the assignee entry form of the
    main window.

    Args:
        main_window: The main window object.

    Returns:
        None
    """

    main_window.ui.assignee_entryform_lblId.clear()
    main_window.ui.assignee_entryform_txtName.clear()
    main_window.ui.assignee_entryform_txtDescription.clear()


def new_assignee(main_window: MainWindow) -> None:
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


def edit_assignee(main_window: MainWindow) -> None:
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
    main_window.ui.assignee_entryform_lblId.setText(str(entity.id))
    main_window.ui.assignee_entryform_txtName.setText(entity.name)
    main_window.ui.assignee_entryform_txtDescription.setPlainText(entity.description)
    main_window.ui.assignee_entryform_txtName.setFocus()
    navigate(main_window, Page.ASSIGNEE_ENTRYFORM)


def delete_assignee(main_window: MainWindow) -> None:
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

    if not askyesno("Confirm delete", "Are you sure you would like to delete the selected record?"):
        return
    selected_id = selected_row_id(main_window.ui.assignee_listingview_tblAssignee)
    global global_assignees
    entity = global_assignees[selected_id]
    delete_by_attrs_dict(Assignee, {"id": entity.id})
    load_assignee_listingview(main_window)


def save_assignee(main_window: MainWindow) -> None:
    """
    Saves the current record to the database.

    If the user cancels the save operation, the function will exit without saving.

    Args:
        main_window: The instance of the main window.

    Returns:
        None
    """

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

    save_by_list([entity])

    load_assignee_listingview(main_window)

    clear_assignee_entryform(main_window)


def back_to_assignee_listingview(main_window: MainWindow) -> None:
    """
    Navigates back to the assignee listing view.

    Args:
        main_window: The instance of the main window.

    Returns:
        None
    """

    clear_assignee_entryform(main_window)

    navigate(main_window, Page.ASSIGNEE_LISTINGVIEW)


def assignees_by_search(main_window: MainWindow, search_text: str) -> None:
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


def connect_assignee_actions(main_window: MainWindow) -> None:
    """
    Connects the actions for the assignee listing view and the assignee entry form.

    Args:
        main_window: The instance of the main window.

    Returns:
        None
    """
    
    main_window.ui.assignee_listingview_btnNew.clicked.connect(lambda: new_assignee(main_window))
    main_window.ui.assignee_listingview_btnEdit.clicked.connect(
        lambda: edit_assignee(main_window)
    )
    main_window.ui.assignee_listingview_btnDelete.clicked.connect(
        lambda: delete_assignee(main_window)
    )
    main_window.ui.assignee_entryform_btnSave.clicked.connect(lambda: save_assignee(main_window))
    main_window.ui.assignee_entryform_btnBack.clicked.connect(lambda: back_to_assignee_listingview(main_window))

    main_window.ui.assignee_listingview_txtSearch.textChanged.connect(
        lambda: assignees_by_search(
            main_window, main_window.ui.assignee_listingview_txtSearch.text().lower()
        )
    )
