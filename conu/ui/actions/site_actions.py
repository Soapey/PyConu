from tkinter.messagebox import askyesno

from conu.classes.Site import Site
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


def load_site_listingview(main_window) -> None:

    global global_sites
    global_sites = select_by_attrs_dict(Site)

    main_window.ui.site_listingview_txtSearch.clear()

    sites_by_search(main_window, None)

    set_site_button_visibility(main_window)

    navigate(main_window, Page.SITE_LISTINGVIEW)


def clear_site_entryform(main_window) -> None:

    main_window.ui.site_entryform_lblId.clear()
    main_window.ui.site_entryform_txtName.clear()
    main_window.ui.site_entryform_txtAddress.clear()
    main_window.ui.site_entryform_txtSuburb.clear()


def new_site(main_window) -> None:

    clear_site_entryform(main_window)

    main_window.ui.site_entryform_txtName.setFocus()

    navigate(main_window, Page.SITE_ENTRYFORM)


def edit_site(main_window) -> None:

    selected_id = selected_row_id(main_window.ui.site_listingview_tblSite)
    global global_sites
    entity = global_sites[selected_id]

    main_window.ui.site_entryform_lblId.setText(str(entity.id))
    main_window.ui.site_entryform_txtName.setText(entity.name)
    main_window.ui.site_entryform_txtAddress.setText(entity.address)
    main_window.ui.site_entryform_txtSuburb.setText(entity.suburb)
    main_window.ui.site_entryform_txtName.setFocus()

    navigate(main_window, Page.SITE_ENTRYFORM)


def delete_site(main_window) -> None:

    if not askyesno(
        "Confirm delete", "Are you sure you would like to delete the selected record?"
    ):
        return

    selected_id = selected_row_id(main_window.ui.site_listingview_tblSite)
    global global_sites
    entity = global_sites[selected_id]

    delete_by_attrs_dict(Site, {"id": entity.id})

    SuccessNotification(
        "Delete Successful", [f"Successfully deleted site: {entity.name}"]
    ).show()

    load_site_listingview(main_window)


def site_entryform_is_valid(main_window) -> bool:

    error_strings = list()

    name = main_window.ui.site_entryform_txtName.text()
    if not name:
        error_strings.append("Name field cannot be blank.")
    else:
        existing_sites = select_by_attrs_dict(Site, {"name": name})
        editing_id = main_window.ui.site_entryform_lblId.text()

        if existing_sites and editing_id:

            existing_site = list(existing_sites.values())[0]

            if existing_site.id != int(editing_id):
                error_strings.append(f"Site: {name}, already exists.")

    if error_strings:
        ErrorNotification("Cannot Save Site", error_strings).show()

    return not bool(error_strings)


def save_site(main_window) -> None:

    if not site_entryform_is_valid(main_window):
        return

    if not askyesno(
        "Confirm save", "Are you sure you would like to save the current record?"
    ):
        return

    entity = Site(
        None
        if len(main_window.ui.site_entryform_lblId.text()) == 0
        else int(main_window.ui.site_entryform_lblId.text()),
        main_window.ui.site_entryform_txtName.text(),
        main_window.ui.site_entryform_txtAddress.text(),
        main_window.ui.site_entryform_txtSuburb.text(),
    )

    save_by_list([entity])

    SuccessNotification(
        "Save Successful", [f"Successfully saved site: {entity.name}"]
    ).show()

    load_site_listingview(main_window)

    clear_site_entryform(main_window)


def back_to_site_listingview(main_window) -> None:

    clear_site_entryform(main_window)

    navigate(main_window, Page.SITE_LISTINGVIEW)


def sites_by_search(main_window, search_text: str) -> None:

    global global_sites

    if not search_text:
        matches = list(global_sites.values())
    else:
        matches = list(
            filter(
                lambda e: search_text
                in "".join(
                    [str(e.id), e.name.lower(), e.address.lower(), e.suburb.lower()]
                ),
                global_sites.values(),
            )
        )

    load_entities_into_table(
        main_window.ui.site_listingview_tblSite,
        matches,
        {"id": "ID", "name": "Name", "address": "Address", "suburb": "Suburb"},
    )


def set_site_button_visibility(main_window):

    if main_window.current_user.permission_level <= 1:
        set_button_visibility(
            [
                main_window.ui.site_listingview_btnNew,
                main_window.ui.site_listingview_btnEdit,
                main_window.ui.site_listingview_btnDelete,
            ],
            is_visible=False,
        )
    else:
        set_button_visibility([main_window.ui.site_listingview_btnNew], is_visible=True)
        set_button_visibility(
            [
                main_window.ui.site_listingview_btnEdit,
                main_window.ui.site_listingview_btnDelete,
            ],
            is_visible=selected_row_id(main_window.ui.site_listingview_tblSite)
            is not None,
        )


def connect_site_actions(main_window) -> None:

    main_window.ui.action_sites.triggered.connect(
        lambda: load_site_listingview(main_window)
    )
    main_window.ui.site_listingview_btnNew.clicked.connect(
        lambda: new_site(main_window)
    )
    main_window.ui.site_listingview_btnEdit.clicked.connect(
        lambda: edit_site(main_window)
    )
    main_window.ui.site_listingview_btnDelete.clicked.connect(
        lambda: delete_site(main_window)
    )
    main_window.ui.site_entryform_btnSave.clicked.connect(
        lambda: save_site(main_window)
    )
    main_window.ui.site_entryform_btnBack.clicked.connect(
        lambda: back_to_site_listingview(main_window)
    )
    main_window.ui.site_listingview_txtSearch.textChanged.connect(
        lambda: sites_by_search(
            main_window, main_window.ui.site_listingview_txtSearch.text().lower()
        )
    )
    main_window.ui.site_listingview_tblSite.itemSelectionChanged.connect(
        lambda: set_site_button_visibility(main_window)
    )
