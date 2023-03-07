from conu.ui.actions.assignee_actions import load_assignee_listingview
from conu.ui.actions.department_actions import load_department_listingview
from conu.ui.actions.form_actions import load_form_listingview
from conu.ui.actions.prioritylevel_actions import load_prioritylevel_listingview
from conu.ui.actions.site_actions import load_site_listingview
from conu.ui.actions.user_actions import load_user_listingview


def connect_menu_actions(main_window):

    main_window.ui.action_logout.triggered.connect(
        lambda: main_window.login_window.log_out_user()
    )
    main_window.ui.action_assignees.triggered.connect(
        lambda: load_assignee_listingview(main_window)
    )
    main_window.ui.action_departments.triggered.connect(
        lambda: load_department_listingview(main_window)
    )
    main_window.ui.action_forms.triggered.connect(
        lambda: load_form_listingview(main_window)
    )
    main_window.ui.action_prioritylevels.triggered.connect(
        lambda: load_prioritylevel_listingview(main_window)
    )
    main_window.ui.action_sites.triggered.connect(
        lambda: load_site_listingview(main_window)
    )
    main_window.ui.action_users.triggered.connect(
        lambda: load_user_listingview(main_window)
    )
    main_window.ui.action_changepassword.triggered.connect(
        lambda: print("Change Password clicked placeholder.")
    )
