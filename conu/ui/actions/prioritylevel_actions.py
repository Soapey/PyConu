from tkinter.messagebox import askyesno

from conu.classes.PriorityLevel import PriorityLevel
from conu.ui.components.Notification import Notification, NotificationColour

from conu.db.SQLiteConnection import (
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


def load_prioritylevel_listingview(main_window) -> None:

    global global_prioritylevels
    global_prioritylevels = select_by_attrs_dict(PriorityLevel)

    main_window.ui.prioritylevel_listingview_txtSearch.clear()

    prioritylevels_by_search(main_window, None)

    set_prioritylevel_button_visibility(main_window, [main_window.ui.prioritylevel_listingview_btnEdit, main_window.ui.prioritylevel_listingview_btnDelete])

    navigate(main_window, Page.PRIORITYLEVEL_LISTINGVIEW)


def clear_prioritylevel_entryform(main_window) -> None:

    main_window.ui.prioritylevel_entryform_lblId.clear()
    main_window.ui.prioritylevel_entryform_txtName.clear()
    main_window.ui.prioritylevel_entryform_spnDaysUntilOverdue.setValue(1)


def new_prioritylevel(main_window) -> None:

    clear_prioritylevel_entryform(main_window)

    main_window.ui.department_entryform_txtName.setFocus()

    navigate(main_window, Page.PRIORITYLEVEL_ENTRYFORM)


def edit_prioritylevel(main_window) -> None:

    selected_id = selected_row_id(main_window.ui.prioritylevel_listingview_tblPriorityLevel)
    global global_prioritylevels
    entity = global_prioritylevels[selected_id]

    main_window.ui.prioritylevel_entryform_lblId.setText(str(entity.id))
    main_window.ui.prioritylevel_entryform_txtName.setText(entity.name)
    main_window.ui.prioritylevel_entryform_spnDaysUntilOverdue.setValue(entity.days_until_overdue)
    main_window.ui.prioritylevel_entryform_txtName.setFocus()

    navigate(main_window, Page.PRIORITYLEVEL_ENTRYFORM)


def delete_prioritylevel(main_window) -> None:

    if not askyesno("Confirm delete", "Are you sure you would like to delete the selected record?"):
        return
    
    selected_id = selected_row_id(main_window.ui.prioritylevel_listingview_tblPriorityLevel)
    global global_prioritylevels
    entity = global_prioritylevels[selected_id]

    delete_by_attrs_dict(PriorityLevel, {"id": entity.id})

    Notification("Delete Successful",[f"Successfully deleted priority level: {entity.name}"], NotificationColour.SUCCESS).show()

    load_prioritylevel_listingview(main_window)


def prioritylevel_entryform_is_valid(main_window) -> bool:

    error_strings = list()

    if not main_window.ui.prioritylevel_entryform_txtName.text():
        error_strings.append("Name field cannot be blank.")

    if error_strings:
        Notification("Cannot Save Priority Level", error_strings, NotificationColour.ERROR).show()

    return not bool(error_strings)


def save_prioritylevel(main_window) -> None:

    if not prioritylevel_entryform_is_valid(main_window):
        return

    if not askyesno("Confirm save", "Are you sure you would like to save the current record?"):
        return

    entity = PriorityLevel(
        None
        if len(main_window.ui.prioritylevel_entryform_lblId.text()) == 0
        else int(main_window.ui.prioritylevel_entryform_lblId.text()),
        main_window.ui.prioritylevel_entryform_txtName.text(), 
        main_window.ui.prioritylevel_entryform_spnDaysUntilOverdue.value(),
    )

    save_by_list([entity])

    Notification("Save Successful", [f"Successfully saved priority level: {entity.name}"], NotificationColour.SUCCESS).show()

    load_prioritylevel_listingview(main_window)

    clear_prioritylevel_entryform(main_window)


def back_to_prioritylevel_listingview(main_window) -> None:

    clear_prioritylevel_entryform(main_window)

    navigate(main_window, Page.PRIORITYLEVEL_LISTINGVIEW)


def prioritylevels_by_search(main_window, search_text: str) -> None:

    global global_prioritylevels

    if not search_text:
        matches = list(global_prioritylevels.values())
    else:
        matches = list(
            filter(
                lambda e: search_text in "".join([str(e.id), e.name.lower()]),
                global_prioritylevels.values(),
            )
        )

    load_entities_into_table(
        main_window.ui.prioritylevel_listingview_tblPriorityLevel,
        matches,
        {"id": "ID", "name": "Name", "days_until_overdue": "Days Until Overdue"},
    )


def set_prioritylevel_button_visibility(main_window, buttons):

    set_button_visibility(
        buttons,
        selected_row_id(main_window.ui.prioritylevel_listingview_tblPriorityLevel) is not None,
    )


def connect_prioritylevel_actions(main_window) -> None:

    main_window.ui.prioritylevel_listingview_btnNew.clicked.connect(
        lambda: new_prioritylevel(main_window)
    )
    main_window.ui.prioritylevel_listingview_btnEdit.clicked.connect(
        lambda: edit_prioritylevel(main_window)
    )
    main_window.ui.prioritylevel_listingview_btnDelete.clicked.connect(
        lambda: delete_prioritylevel(main_window)
    )
    main_window.ui.prioritylevel_entryform_btnSave.clicked.connect(
        lambda: save_prioritylevel(main_window)
    )
    main_window.ui.prioritylevel_entryform_btnBack.clicked.connect(
        lambda: back_to_prioritylevel_listingview(main_window)
    )
    main_window.ui.prioritylevel_listingview_txtSearch.textChanged.connect(
        lambda: prioritylevels_by_search(
            main_window, main_window.ui.prioritylevel_listingview_txtSearch.text().lower()
        )
    )
    main_window.ui.prioritylevel_listingview_tblPriorityLevel.itemSelectionChanged.connect(
        lambda: set_prioritylevel_button_visibility(main_window, [main_window.ui.prioritylevel_listingview_btnEdit, main_window.ui.prioritylevel_listingview_btnDelete])
    )
