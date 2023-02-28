from conu.classes.User import User
from conu.db.SQLiteConnection import select_by_attrs_dict
from conu.helpers import hash_sha512, navigate
from conu.ui.PageEnum import Page
from conu.ui.actions.assignee_actions import load_assignee_listingview
from conu.ui.components.MainWindow import MainWindow


def clear_login(main_window: MainWindow) -> None:
    """
    Clears the username and password fields of the login form.

    Args:
        main_window (object): the main window of the application.
    """
    main_window.ui.login_txtUsername.clear()
    main_window.ui.login_txtPassword.clear()


def log_out_user(main_window: MainWindow) -> None:
    """
    Logs out the current user and navigates to the login page.

    Args:
        main_window (object): the main window of the application.
    """
    main_window.current_user = None
    clear_login(main_window)
    navigate(main_window, Page.LOGIN)


def log_in_user(main_window: MainWindow) -> None:
    """
    Logs in the user with the provided username and password, if they exist in the database,
    and navigates to the assignee listing view.

    Args:
        main_window (object): the main window of the application.

    Returns:
        None
    """
    login_username = main_window.ui.login_txtUsername.text()
    login_password = main_window.ui.login_txtPassword.text()

    if not (login_username and login_password):
        return

    login_password_hash = hash_sha512(login_password)

    matching_users_dict = select_by_attrs_dict(
        User, {"username": login_username, "password": login_password_hash}
    )
    matching_user = list(matching_users_dict.values())[0]

    if matching_users_dict:
        main_window.current_user = matching_user
        load_assignee_listingview(main_window)


def connect_login_actions(main_window: MainWindow) -> None:
    """
    Connects the login button to the log_in_user function.

    Args:
        main_window (object): the main window of the application.

    Returns:
        None
    """
    main_window.ui.login_btnLogin.clicked.connect(lambda: log_in_user(main_window))
