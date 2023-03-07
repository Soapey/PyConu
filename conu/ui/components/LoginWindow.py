from PyQt5.QtWidgets import QMainWindow
from conu.ui.components.Ui_Login import Ui_MainWindow
from conu.ui.components.MainWindow import MainWindow
from conu.classes.User import User
from conu.db.SQLiteConnection import select_by_attrs_dict
from conu.helpers import hash_sha512
from conu.ui.actions.assignee_actions import load_assignee_listingview
from conu.ui.components.Notification import Notification


class LoginWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.main_window = MainWindow(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._connect_window_actions()

    def clear(self) -> None:

        self.ui.login_txtUsername.clear()
        self.ui.login_txtPassword.clear()

    def set_toolbar_permission_visibility(self):

        user = self.main_window.current_user

        if not user:
            return

        admin_toolbars_visible = user.permission_level >= 3

        self.main_window.ui.action_departments.setVisible(admin_toolbars_visible)
        self.main_window.ui.action_users.setVisible(admin_toolbars_visible)

    def log_out_user(self) -> None:

        self.main_window.current_user = None

        self.clear()

        self.ui.login_txtUsername.setFocus(True)

        self.showMaximized()

        self.main_window.close()

    def login_entryform_is_valid(self) -> bool:

        error_strings = list()

        entered_username = self.ui.login_txtUsername.text()
        entered_password = self.ui.login_txtPassword.text()

        if not entered_username:
            error_strings.append("Username field cannot be blank.")

        if not entered_password:
            error_strings.append("Password field cannot be blank.")

        if error_strings:
            Notification("Invalid Login Credentials", error_strings).show()

        return not bool(error_strings)

    def log_in_user(self) -> None:

        if not self.login_entryform_is_valid():
            return

        entered_username = self.ui.login_txtUsername.text()
        entered_password = self.ui.login_txtPassword.text()

        if not (entered_username and entered_password):
            return

        login_password_hash = hash_sha512(entered_password)

        matching_users_dict = select_by_attrs_dict(
            User,
            {
                "username": entered_username,
                "password": login_password_hash,
                "available": 1,
            },
        )

        if matching_users_dict:

            matching_user = list(matching_users_dict.values())[0]

            self.main_window.current_user = matching_user

            self.set_toolbar_permission_visibility()

            load_assignee_listingview(self.main_window)

            self.main_window.showMaximized()

            self.close()

            Notification(
                "Log In Successful",
                [f"Welcome {matching_user.first_name} {matching_user.last_name}"],
            ).show()
        else:
            Notification(
                "Invalid Login Credentials", ["No user matches the given credentials."]
            ).show()

    def _connect_window_actions(self):
        self.ui.login_btnLogin.clicked.connect(lambda: self.log_in_user())
