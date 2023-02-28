from PyQt5.QtWidgets import QMainWindow
from conu.ui.components.Ui_Login import Ui_MainWindow
from conu.ui.actions.login_actions import connect_login_actions
from conu.ui.components.MainWindow import MainWindow


class LoginWindow(QMainWindow):
    def __init__(self, main_window: MainWindow) -> None:
        super().__init__()
        self.main_window = main_window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._connect_window_actions()

    def _connect_window_actions(self):
        connect_login_actions(self, self.main_window)
