from PyQt5.QtWidgets import QMainWindow
from conu.ui.components.Ui_MainWindow import Ui_MainWindow
from conu.ui.actions.assignee_actions import connect_assignee_actions
from conu.ui.actions.department_actions import connect_department_actions


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_user = None
        self._connect_window_actions()

    def _connect_window_actions(self):
        connect_assignee_actions(self)
        connect_department_actions(self)
