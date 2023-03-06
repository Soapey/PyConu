from conu.ui.actions.assignee_actions import load_assignee_listingview
from conu.ui.actions.department_actions import load_department_listingview
from conu.ui.actions.form_actions import load_form_listingview
from conu.ui.actions.prioritylevel_actions import load_prioritylevel_listingview


def connect_menu_actions(main_window):
    main_window.ui.action_assignees.triggered.connect(lambda: load_assignee_listingview(main_window))
    main_window.ui.action_departments.triggered.connect(lambda: load_department_listingview(main_window))
    main_window.ui.action_forms.triggered.connect(lambda: load_form_listingview(main_window))
    main_window.ui.action_prioritylevels.triggered.connect(lambda: load_prioritylevel_listingview(main_window))
