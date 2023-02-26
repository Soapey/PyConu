import sys
from PyQt5.QtWidgets import QApplication
from conu.ui.components.MainWindow import MainWindow
from conu.db.SQLiteConnection import init_db
from conu.ui.actions.login_actions import connect as connect_login, log_out_user
from conu.ui.actions.assignee_actions import connect as connect_assignee


def connect_main_window_actions(main_window):
    connect_login(main_window)
    connect_assignee(main_window)


def start_app():


    app = QApplication(sys.argv)
    
    main_window = MainWindow()

    log_out_user(main_window)

    main_window.showMaximized()

    connect_main_window_actions(main_window)

    sys.exit(app.exec_())

    
if __name__ == "__main__":
    try:
        clean = bool(int(sys.argv[1]))
    except:
        print("First parameter must be database 'clean' boolean.")
        sys.exit()

    init_db(clean=clean)

    start_app()







