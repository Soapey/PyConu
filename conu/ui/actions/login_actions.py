from conu.ui.PageEnum import Page
from conu.helpers import hash_sha512, navigate
from conu.db.SQLiteConnection import get_user_by_credentials
from conu.ui.actions.assignee_actions import load_listingview


def clear_login(main_window):
    main_window.ui.login_txtUsername.clear()
    main_window.ui.login_txtPassword.clear()


def log_out_user(main_window):
    main_window.current_user = None
    clear_login(main_window)
    navigate(main_window, Page.LOGIN)


def log_in_user(main_window):
    
    login_username = main_window.ui.login_txtUsername.text()
    login_password = main_window.ui.login_txtPassword.text()

    if not (login_username and login_password):
        return
    
    login_password_hash = hash_sha512(login_password)

    matching_user = get_user_by_credentials(login_username, login_password_hash)

    if matching_user:
        load_listingview(main_window)


def connect(main_window):

    #main_window.actionProducts.triggered.connect(lambda: navigate_to_listing_view(main_window))
    #main_window.tblProducts.selectionModel().selectionChanged.connect(lambda: on_row_select(main_window))
    #main_window.btnNewProduct.clicked.connect(lambda: new(main_window))

    main_window.ui.login_btnLogin.clicked.connect(lambda: log_in_user(main_window))