from conu.classes.User import User
from conu.db.SQLiteConnection import select_by_attrs_dict
from conu.helpers import hash_sha512
from conu.ui.actions.assignee_actions import load_assignee_listingview


def clear_login(login_window) -> None:
    """
    Clears the username and password fields of the login form.

    Args:
        login_window (object): the login window of the application.
    """
    login_window.ui.login_txtUsername.clear()
    login_window.ui.login_txtPassword.clear()


def set_toolbar_permission_visibility(main_window):

    user = main_window.current_user

    if not user:
        return

    admin_toolbars_visible = user.permission_level >= 3

    main_window.ui.action_departments.setVisible(admin_toolbars_visible)


def log_out_user(login_window, main_window) -> None:
    """
    Logs out the current user and navigates to the login page.

    Args:
        login_window (object): the login window of the application.
        main_window (object): the main window of the application.
    """
    main_window.current_user = None
    clear_login(login_window)
    login_window.showMaximized()
    main_window.close()


def log_in_user(login_window, main_window) -> None:
    """
    Logs in the user with the provided username and password, if they exist in the database,
    and navigates to the assignee listing view.

    Args:
        login_window (object): the login window of the application.
        main_window (object): the main window of the application.

    Returns:
        None
    """
    login_username = login_window.ui.login_txtUsername.text()
    login_password = login_window.ui.login_txtPassword.text()

    if not (login_username and login_password):
        return

    login_password_hash = hash_sha512(login_password)

    matching_users_dict = select_by_attrs_dict(
        User, {"username": login_username, "password": login_password_hash}
    )
    matching_user = list(matching_users_dict.values())[0]

    if matching_users_dict:
        main_window.current_user = matching_user

        set_toolbar_permission_visibility(main_window)

        load_assignee_listingview(main_window)

        main_window.showMaximized()
        login_window.close()


def connect_login_actions(login_window, main_window) -> None:
    """
    Connects the login button to the log_in_user function.

    Args:
        login_window (object): the login window of the application.
        main_window (object): the main window of the application.

    Returns:
        None
    """
    login_window.ui.login_btnLogin.clicked.connect(
        lambda: log_in_user(login_window, main_window)
    )
