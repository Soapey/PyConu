from PyQt5.QtWidgets import QMainWindow
from conu.ui.components.Ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_user = None