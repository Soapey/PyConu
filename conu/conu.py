import sys
from PyQt5.QtWidgets import QApplication
from conu.ui.components.MainWindow import MainWindow
from conu.ui.components.LoginWindow import LoginWindow
from conu.db.SQLiteConnection import init_db, add_test_data
from conu.ui.actions.login_actions import log_out_user


def start_app():

    app = QApplication(sys.argv)

    main_window = MainWindow()

    login_window = LoginWindow(main_window)

    log_out_user(login_window, main_window)

    sys.exit(app.exec_())


if __name__ == "__main__":
    try:
        clean = bool(int(sys.argv[1]))
    except:
        print("First parameter must be database 'clean' boolean.")
        sys.exit()

    try:
        add_data = bool(int(sys.argv[2]))
    except:
        print("Second parameter must be 'add_test_data' boolean.")
        sys.exit()

    init_db(clean=clean)

    if add_data:
        add_test_data()

    start_app()
