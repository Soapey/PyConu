from datetime import date
from tkinter.messagebox import askyesno

from conu.classes.ServiceTracker import ServiceTracker
from conu.classes.Item import Item
from conu.ui.components.Notification import Notification
from conu.ui.components.SelectWindow import SelectWindow

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


def load_servicetracker_listingview(main_window) -> None:

    global global_servicetrackers
    global_servicetrackers = select_by_attrs_dict(ServiceTracker)

    main_window.ui.servicetracker_listingview_txtSearch.clear()

    servicetrackers_by_search(main_window, None)

    set_servicetracker_button_visibility(main_window)

    navigate(main_window, Page.SERVICETRACKER_LISTINGVIEW)


def clear_servicetracker_entryform(main_window) -> None:

    main_window.ui.servicetracker_entryform_lblId.clear()
    main_window.ui.servicetracker_entryform_lblItem.clear()
    main_window.ui.servicetracker_entryform_dteCalibrationDate.setDate(date.today())
    main_window.ui.servicetracker_entryform_spnCurrentUnits.setValue(0)
    main_window.ui.servicetracker_entryform_spnAverageUnitsPerDay.setValue(0)
    main_window.ui.servicetracker_entryform_spnServiceDueUnits.setValue(0)
    main_window.ui.servicetracker_entryform_spnServiceIntervalUnits.setValue(0)


def new_servicetracker(main_window) -> None:

    clear_servicetracker_entryform(main_window)

    main_window.ui.servicetracker_entryform_dteCalibrationDate.setFocus()

    navigate(main_window, Page.SERVICETRACKER_ENTRYFORM)


def edit_servicetracker(main_window) -> None:

    selected_id = selected_row_id(main_window.ui.servicetracker_listingview_tblServiceTracker)
    global global_servicetrackers
    entity = global_servicetrackers[selected_id]

    global global_items
    global_items = select_by_attrs_dict(Item)

    main_window.ui.servicetracker_entryform_lblId.setText(str(entity.id))
    main_window.ui.servicetracker_entryform_lblItem.setText(global_items[entity.item_id].name)
    main_window.ui.servicetracker_entryform_dteCalibrationDate.setDate(entity.units_calibration_date)
    main_window.ui.servicetracker_entryform_spnCurrentUnits.setValue(entity.current_units)
    main_window.ui.servicetracker_entryform_spnAverageUnitsPerDay.setValue(entity.average_units_per_day)
    main_window.ui.servicetracker_entryform_spnServiceDueUnits.setValue(entity.service_due_units)
    main_window.ui.servicetracker_entryform_spnServiceIntervalUnits.setValue(entity.service_interval)

    main_window.ui.servicetracker_entryform_dteCalibrationDate.setFocus()

    navigate(main_window, Page.SERVICETRACKER_ENTRYFORM)


def delete_servicetracker(main_window) -> None:

    if not askyesno("Confirm delete", "Are you sure you would like to delete the selected record?"):
        return
    
    selected_id = selected_row_id(main_window.ui.servicetracker_listingview_tblServiceTracker)
    global global_servicetrackers
    global global_items

    entity = global_servicetrackers[selected_id]
    item = global_items(entity.item_id)

    delete_by_attrs_dict(ServiceTracker, {"id": entity.id})

    Notification("Delete Successful", [f"Successfully deleted service tracker for: {item.name}"]).show()

    load_servicetracker_listingview(main_window)


def servicetracker_entryform_is_valid(main_window) -> bool:

    error_strings = list()


    if not main_window.ui.servicetracker_entryform_lblId.text():
        error_strings.append("An item must be selected.")

    if error_strings:
        Notification("Cannot Save Service Tracker", error_strings).show()

    return not bool(error_strings)


def save_servicetracker(main_window) -> None:

    if not servicetracker_entryform_is_valid(main_window):
        return

    if not askyesno(
        "Confirm save", "Are you sure you would like to save the current record?"
    ):
        return

    item = main_window.ui.servicetracker_entryform_lblId.property("object")

    entity = ServiceTracker(
        id=None
        if len(main_window.ui.servicetracker_entryform_lblId.text()) == 0
        else int(main_window.ui.servicetracker_entryform_lblId.text()),
        item_id=item.id,
        units_calibration_date=main_window.ui.servicetracker_entryform_dteCalibrationDate.date(),
        current_units=main_window.ui.servicetracker_entryform_spnCurrentUnits.value(),
        average_units_per_day=main_window.ui.servicetracker_entryform_spnAverageUnitsPerDay.value(),
        service_due_units=main_window.ui.servicetracker_entryform_spnServiceDueUnits.value(),
        service_interval=main_window.ui.servicetracker_entryform_spnServiceIntervalUnits.value(),
    )

    save_by_list([entity])

    Notification("Save Successful", [f"Successfully saved service tracker: {entity.name}"]).show()

    load_servicetracker_listingview(main_window)

    clear_servicetracker_entryform(main_window)


def back_to_servicetracker_listingview(main_window) -> None:

    clear_servicetracker_entryform(main_window)

    navigate(main_window, Page.SERVICETRACKER_LISTINGVIEW)


def servicetrackers_by_search(main_window, search_text: str) -> None:

    global global_servicetrackers
    global global_items

    if not search_text:
        matches = list(global_servicetrackers.values())
    else:
        matches = list(
            filter(
                lambda e: search_text in "".join([str(e.id), global_items[e.item_id].name.lower()]),
                global_servicetrackers.values(),
            )
        )

    load_entities_into_table(
        main_window.ui.servicetracker_listingview_tblServiceTracker,
        matches,
        {"id": "ID", 
         "item_id": "Item", 
         "units_calibration_date": "Calibration Date", 
         "current_units": "Current Units", 
         "average_units_per_day": "Average Units per Day", 
         "service_due_units": "Service Due Units", 
         "service_interval": "Service Interval"},
    )


def set_servicetracker_button_visibility(main_window):

    if main_window.current_user.permission_level <= 1:
        set_button_visibility([
            main_window.ui.servicetracker_listingview_btnNew,
            main_window.ui.servicetracker_listingview_btnEdit,
            main_window.ui.servicetracker_listingview_btnDelete,
            ],
            is_visible=False)
    else:
        set_button_visibility([main_window.ui.servicetracker_listingview_btnNew], is_visible=True)
        set_button_visibility([
            main_window.ui.servicetracker_listingview_btnEdit,
            main_window.ui.servicetracker_listingview_btnDelete
            ],
            is_visible=selected_row_id(main_window.ui.servicetracker_listingview_tblServiceTracker) is not None,
        )


def select_item(main_window):

    select_window = SelectWindow(Item, main_window.ui.servicetracker_entryform_lblItem.setText, "name", main_window.ui.servicetracker_entryform_lblItem.setProperty, {"id": "ID", "name": "Name", "comments": "Comments"})


def connect_servicetracker_actions(main_window) -> None:

    main_window.ui.servicetracker_listingview_btnNew.clicked.connect(
        lambda: new_servicetracker(main_window)
    )
    main_window.ui.servicetracker_listingview_btnEdit.clicked.connect(
        lambda: edit_servicetracker(main_window)
    )
    main_window.ui.servicetracker_listingview_btnDelete.clicked.connect(
        lambda: delete_servicetracker(main_window)
    )
    main_window.ui.servicetracker_entryform_btnSelectItem.clicked.connect(
        lambda: select_item(main_window)
    )
    main_window.ui.servicetracker_entryform_btnSave.clicked.connect(
        lambda: save_servicetracker(main_window)
    )
    main_window.ui.servicetracker_entryform_btnBack.clicked.connect(
        lambda: back_to_servicetracker_listingview(main_window)
    )
    main_window.ui.servicetracker_listingview_txtSearch.textChanged.connect(
        lambda: servicetrackers_by_search(
            main_window, main_window.ui.servicetracker_listingview_txtSearch.text().lower()
        )
    )
    main_window.ui.servicetracker_listingview_tblServiceTracker.itemSelectionChanged.connect(
        lambda: set_servicetracker_button_visibility(main_window)
    )
