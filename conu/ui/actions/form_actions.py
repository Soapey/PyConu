from tkinter.messagebox import askyesno

from conu.classes.Form import Form
from conu.db.SQLiteConnection import (
    delete_by_attrs_dict,
    save_by_list,
    select_by_attrs_dict,
)
from conu.helpers import (
    load_entities_into_table,
    navigate,
    selected_row_id,
    create_notification,
)
from conu.ui.PageEnum import Page
from conu.helpers import select_file_path


def load_form_listingview(main_window) -> None:

    global global_forms
    global_forms = select_by_attrs_dict(Form)

    main_window.ui.form_listingview_txtSearch.clear()

    forms_by_search(main_window, None)

    navigate(main_window, Page.FORM_LISTINGVIEW)


def clear_form_entryform(main_window) -> None:

    main_window.ui.form_entryform_lblId.clear()
    main_window.ui.form_entryform_txtName.clear()
    main_window.ui.form_entryform_txtPath.clear()


def new_form(main_window) -> None:

    clear_form_entryform(main_window)
    main_window.ui.form_entryform_txtName.setFocus()

    print("entryform ready!")

    navigate(main_window, Page.FORM_ENTRYFORM)


def edit_form(main_window) -> None:

    selected_id = selected_row_id(main_window.ui.form_listingview_tblForm)

    global global_forms
    entity = global_forms[selected_id]
    main_window.ui.form_entryform_lblId.setText(str(entity.id))
    main_window.ui.form_entryform_txtName.setText(entity.name)
    main_window.ui.form_entryform_txtPath.setText(entity.path)
    main_window.ui.form_entryform_txtName.setFocus()
    navigate(main_window, Page.FORM_ENTRYFORM)


def delete_form(main_window) -> None:

    if not askyesno(
        "Confirm delete", "Are you sure you would like to delete the selected record?"
    ):
        return
    selected_id = selected_row_id(main_window.ui.form_listingview_tblForm)
    global global_forms
    entity = global_forms[selected_id]
    delete_by_attrs_dict(Form, {"id": entity.id})
    create_notification(
        "Delete Successful", f"Successfully deleted form: {entity.name}", "74c69d"
    )
    load_form_listingview(main_window)


def form_entryform_is_valid(main_window) -> bool:

    error_strings = list()

    entered_name = main_window.ui.form_entryform_txtName.text()
    entered_path = main_window.ui.form_entryform_txtPath.text()

    if not entered_name:
        error_strings.append("Name field cannot be blank.")

    if not entered_path:
        error_strings.append("Path field cannot be blank.")

    if error_strings:
        create_notification("Cannot Save Form", error_strings, "red")
        return False

    return True


def save_form(main_window) -> None:

    if not form_entryform_is_valid(main_window):
        return

    if not askyesno(
        "Confirm save", "Are you sure you would like to save the current record?"
    ):
        return

    entity = Form(
        None
        if len(main_window.ui.form_entryform_lblId.text()) == 0
        else int(main_window.ui.form_entryform_lblId.text()),
        main_window.ui.form_entryform_txtName.text(),
        main_window.ui.form_entryform_txtPath.text(),
    )

    save_by_list([entity])

    create_notification(
        "Save Successful", f"Successfully saved form: {entity.name}", "74c69d"
    )

    load_form_listingview(main_window)

    clear_form_entryform(main_window)


def back_to_form_listingview(main_window) -> None:

    clear_form_entryform(main_window)

    navigate(main_window, Page.FORM_LISTINGVIEW)


def forms_by_search(main_window, search_text: str) -> None:

    global global_forms

    if not search_text:
        matches = list(global_forms.values())
    else:
        matches = list(
            filter(
                lambda e: search_text in "".join([str(e.id), e.name.lower()]),
                global_forms.values(),
            )
        )

    load_entities_into_table(
        main_window.ui.form_listingview_tblForm,
        matches,
        {"id": "ID", "name": "Name", "path": "Path"},
    )


def select_form_filepath(main_window):

    filepath: str = None
    try:
        filepath = select_file_path()
    except:
        pass

    if filepath:
        main_window.ui.form_entryform_txtPath.setText(filepath)


def connect_form_actions(main_window) -> None:

    main_window.ui.form_listingview_btnNew.clicked.connect(
        lambda: new_form(main_window)
    )
    main_window.ui.form_listingview_btnEdit.clicked.connect(
        lambda: edit_form(main_window)
    )
    main_window.ui.form_listingview_btnDelete.clicked.connect(
        lambda: delete_form(main_window)
    )
    main_window.ui.form_entryform_btnSave.clicked.connect(
        lambda: save_form(main_window)
    )
    main_window.ui.form_entryform_btnBack.clicked.connect(
        lambda: back_to_form_listingview(main_window)
    )
    main_window.ui.form_listingview_txtSearch.textChanged.connect(
        lambda: forms_by_search(
            main_window, main_window.ui.form_listingview_txtSearch.text().lower()
        )
    )
    main_window.ui.form_entryform_btnSelectPath.clicked.connect(
        lambda: select_form_filepath(main_window)
    )
