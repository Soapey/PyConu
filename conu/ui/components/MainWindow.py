from PyQt5.QtWidgets import QMainWindow
from conu.ui.components.Ui_MainWindow import Ui_MainWindow
from conu.ui.actions.assignee_actions import connect_assignee_actions
from conu.ui.actions.department_actions import connect_department_actions
from conu.ui.actions.form_actions import connect_form_actions
from conu.ui.actions.prioritylevel_actions import connect_prioritylevel_actions
from conu.ui.actions.site_actions import connect_site_actions
from conu.ui.actions.user_actions import connect_user_actions
from conu.ui.actions.item_actions import connect_item_actions
from conu.ui.actions.servicetracker_actions import connect_servicetracker_actions
from conu.ui.actions.workorder_actions import connect_workorder_actions


class MainWindow(QMainWindow):
    def __init__(self, login_window) -> None:
        super().__init__()
        self.login_window = login_window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_user = None
        self._connect_window_actions()

    def _connect_window_actions(self):
        connect_assignee_actions(self)
        connect_department_actions(self)
        connect_form_actions(self)
        connect_prioritylevel_actions(self)
        connect_site_actions(self)
        connect_user_actions(self)
        connect_item_actions(self)
        connect_servicetracker_actions(self)
        connect_workorder_actions(self)
