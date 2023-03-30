from tkinter.messagebox import askyesno

from conu.classes.Form import Form
from conu.ui.components.Notification import SuccessNotification, ErrorNotification
from conu.db.helpers import (
    delete_by_attrs_dict,
    save_by_list,
    select_by_attrs_dict,
)
from conu.helpers import (
    load_entities_into_table,
    navigate,
    selected_row_id,
    set_button_visibility,
)
from conu.ui.PageEnum import Page
from conu.helpers import select_file_path


def load_form_listingview(main_window) -> None:

    global global_forms
    global_forms = select_by_attrs_dict(Form)

    main_window.ui.form_listingview_txtSearch.clear()

    forms_by_search(main_window, None)

    set_form_button_visibility(main_window)

    navigate(main_window, Page.FORM_LISTINGVIEW)


def clear_form_entryform(main_window) -> None:

    main_window.ui.form_entryform_lblId.clear()
    main_window.ui.form_entryform_txtName.clear()
    main_window.ui.form_entryform_txtPath.clear()


def new_form(main_window) -> None:

    clear_form_entryform(main_window)

    main_window.ui.form_entryform_txtName.setFocus()

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

    SuccessNotification(
        "Delete Successful", [f"Successfully deleted form: {entity.name}"]
    ).show()

    load_form_listingview(main_window)


def export_form_table(main_window):

    Form.get_listingview_table_data(main_window, export_to_excel=True)


def form_entryform_is_valid(main_window) -> bool:

    error_strings = list()

    name = main_window.ui.form_entryform_txtName.text()
    if not name:
        error_strings.append("Name field cannot be blank.")
    else:
        existing_forms = select_by_attrs_dict(Form, {"name": name})
        editing_id = main_window.ui.form_entryform_lblId.text()

        if existing_forms and editing_id:

            existing_form = list(existing_forms.values())[0]

            if existing_form.id != int(editing_id):
                error_strings.append(f"Form: {name}, already exists.")

    path = main_window.ui.form_entryform_txtPath.text()
    if not path:
        error_strings.append("Path field cannot be blank.")

    if error_strings:
        ErrorNotification("Cannot Save Form", error_strings).show()

    return not bool(error_strings)


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

    SuccessNotification(
        "Save Successful", [f"Successfully saved form: {entity.name}"]
    ).show()

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


def set_form_button_visibility(main_window):

    if main_window.current_user.permission_level <= 1:
        set_button_visibility(
            [
                main_window.ui.form_listingview_btnNew,
                main_window.ui.form_listingview_btnEdit,
                main_window.ui.form_listingview_btnDelete,
            ],
            is_visible=False,
        )
    else:
        set_button_visibility([main_window.ui.form_listingview_btnNew], is_visible=True)
        set_button_visibility(
            [
                main_window.ui.form_listingview_btnEdit,
                main_window.ui.form_listingview_btnDelete,
            ],
            is_visible=selected_row_id(main_window.ui.form_listingview_tblForm)
            is not None,
        )


def connect_form_actions(main_window) -> None:

    main_window.ui.action_forms.triggered.connect(
        lambda: load_form_listingview(main_window)
    )
    main_window.ui.form_listingview_btnNew.clicked.connect(
        lambda: new_form(main_window)
    )
    main_window.ui.form_listingview_btnEdit.clicked.connect(
        lambda: edit_form(main_window)
    )
    main_window.ui.form_listingview_btnDelete.clicked.connect(
        lambda: delete_form(main_window)
    )
    main_window.ui.form_listingview_btnExportTable.clicked.connect(
        lambda: export_form_table(main_window)
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
    main_window.ui.form_listingview_tblForm.itemSelectionChanged.connect(
        lambda: set_form_button_visibility(main_window)
    )
