from tkinter.messagebox import askyesno

from conu.classes.ServiceTracker import ServiceTracker
from conu.classes.WorkOrder import WorkOrder
from conu.classes.RecurringWorkOrder import RecurringWorkOrder
from conu.ui.components.Notification import Notification

from conu.db.helpers import (
    delete_by_attrs_dict,
    select_by_attrs_dict,
    save_by_list,
)
from conu.helpers import (
    load_query_rows_into_table,
    navigate,
    selected_row_id,
    set_button_visibility,
)
from conu.ui.PageEnum import Page


def load_due_listingview(main_window) -> None:

    user_id = main_window.current_user.id
    workorders = WorkOrder.get_by_user_departments(user_id)
    recurringworkorders = RecurringWorkOrder.get_by_user_departments(user_id)
    servicetrackers = ServiceTracker.get_by_user_departments(user_id)

    entities_list = (
        list(workorders.values())
        + list(recurringworkorders.values())
        + list(servicetrackers.values())
    )
    global global_due_table_data
    global_due_table_data = list()
    for entity in entities_list:
        global_due_table_data.append(
            (
                entity.id,
                entity.due_listingview_items(),
                entity.due_listingview_summary(),
                entity.due_listingview_assignees(),
            )
        )

    due_items_by_search(main_window)

    navigate(main_window, Page.DUE_LISTINGVIEW)


def due_items_by_search(main_window) -> None:

    search_text = main_window.ui.due_listingview_txtSearch.text().lower()

    global global_due_table_data

    if not search_text:
        matches = global_due_table_data
    else:
        matches = list(
            filter(
                lambda tup: search_text
                in "".join(
                    [
                        str(tup[0]),
                        str(tup[1]),
                        str(tup[2]),
                        str(tup[3]),
                    ]
                ),
                global_due_table_data,
            )
        )

    load_query_rows_into_table(
        main_window.ui.due_listingview_tblDue,
        matches,
        {
            "ID": (0, str),
            "Items": (1, None),
            "Summary": (2, None),
            "Assignees": (3, None),
        },
    )

    pass


def set_due_button_visibility(main_window):

    if main_window.current_user.permission_level <= 1:
        set_button_visibility(
            [
                main_window.ui.due_listingview_btnRaise,
            ],
            is_visible=False,
        )
    else:
        set_button_visibility(
            [main_window.ui.due_listingview_btnRaise], is_visible=True
        )
        set_button_visibility(
            [
                main_window.ui.due_listingview_btnRaise,
            ],
            is_visible=selected_row_id(main_window.ui.due_listingview_tblDue)
            is not None,
        )


def connect_due_actions(main_window) -> None:

    main_window.ui.action_dueitems.triggered.connect(
        lambda: load_due_listingview(main_window)
    )
    main_window.ui.due_listingview_txtSearch.textChanged.connect(
        lambda: due_items_by_search(main_window)
    )
    main_window.ui.due_listingview_tblDue.itemSelectionChanged.connect(
        lambda: set_due_button_visibility(main_window)
    )
    main_window.ui.due_listingview_btnRaise.clicked.connect(
        lambda: print("Raise clicked!")
    )
