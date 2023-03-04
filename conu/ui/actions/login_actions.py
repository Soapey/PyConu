from conu.classes.User import User
from conu.db.SQLiteConnection import select_by_attrs_dict
from conu.helpers import hash_sha512, create_notification
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


def login_entryform_is_valid(login_window) -> bool:

    error_strings = list()

    entered_username = login_window.ui.login_txtUsername.text()
    entered_password = login_window.ui.login_txtPassword.text()

    if not entered_username:
        error_strings.append("Username field cannot be blank.")

    if not entered_password:
        error_strings.append("Password field cannot be blank.")

    if error_strings:
        create_notification("Invalid Login Credentials", error_strings, "red")
        return False

    return True


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

        create_notification(
            "Log In Successful",
            [f"Welcome {matching_user.first_name} {matching_user.last_name}"],
            "#74c69d",
        )
    else:
        create_notification(
            "Invalid Login Credentials",
            ["No user matches the given credentials."],
            "red",
        )


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
