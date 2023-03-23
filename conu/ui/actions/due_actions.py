from conu.classes.ServiceTracker import ServiceTracker
from conu.classes.WorkOrder import WorkOrder
from conu.classes.RecurringWorkOrder import RecurringWorkOrder
from conu.ui.actions.workorder_actions import edit_workorder

from conu.helpers import (
    load_query_rows_into_table,
    navigate,
    selected_row_id,
    set_button_visibility,
)
from conu.ui.PageEnum import Page


def load_due_listingview(main_window) -> None:

    user_id = main_window.current_user.id
    workorders = list(
        filter(
            lambda e: e.is_due(), WorkOrder.get_by_user_departments(user_id).values()
        )
    )
    recurringworkorders = list(
        filter(
            lambda e: e.is_due(),
            RecurringWorkOrder.get_by_user_departments(user_id).values(),
        )
    )
    servicetrackers = list(
        filter(
            lambda e: e.is_due(),
            ServiceTracker.get_by_user_departments(user_id).values(),
        )
    )

    entities_list = workorders + recurringworkorders + servicetrackers
    global global_due_table_data
    global_due_table_data = list()
    for entity in entities_list:
        global_due_table_data.append(
            (
                entity.id,
                entity.__class__.__name__,
                entity.due_listingview_items(),
                entity.due_listingview_summary(),
                entity.due_listingview_assignees(),
            )
        )

    due_items_by_search(main_window)

    set_due_button_visibility(main_window)

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
                        str(tup[4]),
                    ]
                ).lower(),
                global_due_table_data,
            )
        )

    load_query_rows_into_table(
        main_window.ui.due_listingview_tblDue,
        matches,
        {
            "ID": (0, str),
            "Type": (1, None),
            "Items": (2, None),
            "Summary": (3, None),
            "Assignees": (4, None),
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
            [
                main_window.ui.due_listingview_btnRaise,
            ],
            is_visible=selected_row_id(main_window.ui.due_listingview_tblDue)
            is not None,
        )


def raise_workorder(main_window, workorder_id):

    workorders = WorkOrder.get()
    entity = workorders[workorder_id]
    edit_workorder(main_window, entity)


def raise_recurringworkorder(main_window, recurringworkorder_id):

    recurringworkorders = RecurringWorkOrder.get()
    entity = recurringworkorders[recurringworkorder_id]

    workorder_entity = WorkOrder(
        None,
        entity.site_id,
        entity.department_id,
        entity.prioritylevel_id,
        entity.task_description,
        entity.comments,
        None,
        None,
        None,
        None,
        None,
        None,
    )

    edit_workorder(main_window, workorder_entity, recurringworkorder_id)


def raise_servicetracker(main_window, servicetracker_id):

    servicetrackers = ServiceTracker.get_by_user_departments(
        main_window.current_user.id
    )
    entity = servicetrackers[servicetracker_id]

    workorder_entity = WorkOrder(
        None,
        None,
        None,
        None,
        entity.__str__(),
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )

    edit_workorder(main_window, workorder_entity, None, servicetracker_id)


def raise_due_item(main_window):

    tbl = main_window.ui.due_listingview_tblDue

    selected_items = tbl.selectedItems()

    if not selected_items:
        return

    selected_id = int(selected_items[0].text())
    selected_type = selected_items[1].text().lower()

    if selected_type == "workorder":
        raise_workorder(main_window, selected_id)
    elif selected_type == "recurringworkorder":
        raise_recurringworkorder(main_window, selected_id)
    elif selected_type == "servicetracker":
        raise_servicetracker(main_window, selected_id)


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
        lambda: raise_due_item(main_window)
    )
