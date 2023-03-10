import sys
from PyQt5.QtWidgets import QApplication
from conu.ui.components.LoginWindow import LoginWindow
from conu.db.helpers import init_db, add_test_data


def start_app():

    app = QApplication(sys.argv)

    login_window = LoginWindow()

    login_window.log_out_user()

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
