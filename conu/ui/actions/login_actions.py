from conu.classes.User import User
from conu.db.SQLiteConnection import select_by_attrs_dict
from conu.helpers import hash_sha512
from conu.ui.actions.assignee_actions import load_assignee_listingview
from conu.ui.components.Notification import Notification


def clear_login(login_window) -> None:

    login_window.ui.login_txtUsername.clear()
    login_window.ui.login_txtPassword.clear()


def set_toolbar_permission_visibility(main_window):

    user = main_window.current_user

    if not user:
        return

    admin_toolbars_visible = user.permission_level >= 3

    main_window.ui.action_departments.setVisible(admin_toolbars_visible)


def log_out_user(login_window, main_window) -> None:

    main_window.current_user = None

    clear_login(login_window)

    login_window.showMaximized()

    main_window.close()


def login_entryform_is_valid(login_window) -> bool:

    error_strings = list()

    entered_username = login_window.ui.login_txtUsername.text()
    entered_password = login_window.ui.login_txtPassword.text()

    if not entered_username:
        error_strings.append("Username field cannot be blank.")

    if not entered_password:
        error_strings.append("Password field cannot be blank.")

    if error_strings:
        Notification("Invalid Login Credentials", error_strings).show()

    return not bool(error_strings)


def log_in_user(login_window, main_window) -> None:

    if not login_entryform_is_valid(login_window):
        return

    entered_username = login_window.ui.login_txtUsername.text()
    entered_password = login_window.ui.login_txtPassword.text()

    if not (entered_username and entered_password):
        return

    login_password_hash = hash_sha512(entered_password)

    matching_users_dict = select_by_attrs_dict(
        User, {"username": entered_username, "password": login_password_hash}
    )

    if matching_users_dict:

        matching_user = list(matching_users_dict.values())[0]

        main_window.current_user = matching_user

        set_toolbar_permission_visibility(main_window)

        load_assignee_listingview(main_window)

        main_window.showMaximized()

        login_window.close()

        Notification("Log In Successful", [f"Welcome {matching_user.first_name} {matching_user.last_name}"]).show()
    else:
        Notification("Invalid Login Credentials", ["No user matches the given credentials."]).show()


def connect_login_actions(login_window, main_window) -> None:

    login_window.ui.login_btnLogin.clicked.connect(lambda: log_in_user(login_window, main_window))
