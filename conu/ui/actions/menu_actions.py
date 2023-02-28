from conu.ui.actions.assignee_actions import load_assignee_listingview
from conu.ui.actions.department_actions import load_department_listingview


def connect_menu_actions(main_window):
    main_window.ui.action_assignees.triggered.connect(
        lambda: load_assignee_listingview(main_window)
    )
    main_window.ui.action_departments.triggered.connect(
        lambda: load_department_listingview(main_window)
    )
