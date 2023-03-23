from tkinter.messagebox import askyesno

from conu.classes.Department import Department
from conu.ui.components.Notification import SuccessNotification, ErrorNotification

from conu.db.helpers import (
    delete_by_attrs_dict,
    select_by_attrs_dict,
    save_by_list,
)
from conu.helpers import (
    load_entities_into_table,
    navigate,
    selected_row_id,
    set_button_visibility,
)
from conu.ui.PageEnum import Page


def load_department_listingview(main_window) -> None:

    global global_departments
    global_departments = select_by_attrs_dict(Department)

    main_window.ui.department_listingview_txtSearch.clear()

    departments_by_search(main_window, None)

    set_department_button_visibility(main_window)

    navigate(main_window, Page.DEPARTMENT_LISTINGVIEW)


def clear_department_entryform(main_window) -> None:

    main_window.ui.department_entryform_lblId.clear()
    main_window.ui.department_entryform_txtName.clear()


def new_department(main_window) -> None:

    clear_department_entryform(main_window)
    main_window.ui.department_entryform_txtName.setFocus()
    navigate(main_window, Page.DEPARTMENT_ENTRYFORM)


def edit_department(main_window) -> None:

    selected_id = selected_row_id(main_window.ui.department_listingview_tblDepartment)
    global global_departments
    entity = global_departments[selected_id]
    main_window.ui.department_entryform_lblId.setText(str(entity.id))
    main_window.ui.department_entryform_txtName.setText(entity.name)
    main_window.ui.department_entryform_txtName.setFocus()
    navigate(main_window, Page.DEPARTMENT_ENTRYFORM)


def delete_department(main_window) -> None:

    if not askyesno(
        "Confirm delete", "Are you sure you would like to delete the selected record?"
    ):
        return

    selected_id = selected_row_id(main_window.ui.department_listingview_tblDepartment)
    global global_departments
    entity = global_departments[selected_id]

    delete_by_attrs_dict(Department, {"id": entity.id})

    SuccessNotification(
        "Delete Successful", [f"Successfully deleted department: {entity.name}"]
    ).show()

    load_department_listingview(main_window)


def department_entryform_is_valid(main_window) -> bool:

    error_strings = list()

    name = main_window.ui.department_entryform_txtName.text()
    if not name:
        error_strings.append("Name field cannot be blank.")
    else:
        existing_departments = select_by_attrs_dict(Department, {"name": name})
        editing_id = main_window.ui.department_entryform_lblId.text()

        if existing_departments and editing_id:

            existing_department = list(existing_departments.values())[0]

            if existing_department.id != int(editing_id):
                error_strings.append(f"Department: {name}, already exists.")

    if error_strings:
        ErrorNotification("Cannot Save Department", error_strings).show()

    return not bool(error_strings)


def save_department(main_window) -> None:

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

    SuccessNotification(
        "Save Successful", [f"Successfully saved department: {entity.name}"]
    ).show()

    load_department_listingview(main_window)

    clear_department_entryform(main_window)


def back_to_department_listingview(main_window) -> None:

    clear_department_entryform(main_window)

    navigate(main_window, Page.DEPARTMENT_LISTINGVIEW)


def departments_by_search(main_window, search_text: str) -> None:

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

    if main_window.current_user.permission_level <= 1:
        set_button_visibility(
            [
                main_window.ui.department_listingview_btnNew,
                main_window.ui.department_listingview_btnEdit,
                main_window.ui.department_listingview_btnDelete,
            ],
            is_visible=False,
        )
    else:
        set_button_visibility(
            [main_window.ui.department_listingview_btnNew], is_visible=True
        )
        set_button_visibility(
            [
                main_window.ui.department_listingview_btnEdit,
                main_window.ui.department_listingview_btnDelete,
            ],
            is_visible=selected_row_id(
                main_window.ui.department_listingview_tblDepartment
            )
            is not None,
        )


def connect_department_actions(main_window) -> None:

    main_window.ui.action_departments.triggered.connect(
        lambda: load_department_listingview(main_window)
    )
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
