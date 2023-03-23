from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox
from tkinter.messagebox import askyesno

from conu.classes.User import User
from conu.classes.UserDepartment import UserDepartment
from conu.classes.Department import Department
from conu.db.helpers import (
    delete_by_attrs_dict,
    get_by_user_departments,
    save_by_list,
    select_by_attrs_dict,
)
from conu.helpers import (
    clear_widget_children,
    load_entities_into_table,
    navigate,
    selected_row_id,
    set_button_visibility,
    hash_sha512,
    is_valid_email,
)
from conu.ui.components.Notification import Notification
from conu.ui.PageEnum import Page


user_department_ids = set()


def load_user_listingview(main_window) -> None:

    global global_users
    global_users = get_by_user_departments(User, main_window.current_user.id)

    main_window.ui.user_listingview_txtSearch.clear()

    users_by_search(main_window, None)

    set_user_button_visibility(main_window)

    navigate(main_window, Page.USER_LISTINGVIEW)


def clear_user_entryform(main_window, user_id: int = None) -> None:

    main_window.ui.user_entryform_lblId.clear()
    main_window.ui.user_entryform_txtFirstName.clear()
    main_window.ui.user_entryform_txtLastName.clear()
    main_window.ui.user_entryform_txtJobTitle.clear()
    main_window.ui.user_entryform_txtEmailAddress.clear()
    main_window.ui.user_entryform_txtUsername.clear()
    main_window.ui.user_entryform_txtOldPassword.clear()
    main_window.ui.user_entryform_txtNewPassword.clear()
    main_window.ui.user_entryform_spnPermissionLevel.setValue(1)
    main_window.ui.user_entryform_spnPermissionLevel.setMaximum(
        main_window.current_user.permission_level
    )
    main_window.ui.user_entryform_chkAvailable.setChecked(True)

    main_window.ui.user_entryform_spnPermissionLevel.setEnabled(True)
    main_window.ui.user_entryform_groupDepartments.setEnabled(True)

    vboxDepartments = (
        main_window.ui.user_entryform_vboxDepartments
    )  # Get assignee departments vertical box layout
    vboxDepartments.setAlignment(Qt.AlignTop)

    clear_widget_children(vboxDepartments)

    # Retrieve global_departments and global_assigneedepartments using select_by_attrs_dict function
    global global_departments
    global global_userdepartments
    global_departments = select_by_attrs_dict(Department)
    global_userdepartments = select_by_attrs_dict(UserDepartment)

    # Create a set to store the IDs of departments assigned to the assignee, if an assignee ID has been provided
    global user_department_ids
    if user_id:
        user_department_ids = {
            ud.department_id
            for ud in global_userdepartments.values()
            if ud.user_id == user_id
        }
    else:
        user_department_ids = set()

    # Loop through each department and create a QCheckBox widget for it
    for department in list(global_departments.values()):

        # Create a QCheckBox widget with the department name and add it to the vbox_departments layout
        checkbox = QCheckBox(department.name, main_window.ui.page_user_entryform)
        checkbox.setProperty("object", department)
        checkbox.setChecked(False)  # Set the checkbox to unchecked by default

        # Check if the department is assigned to the assignee, and if so, set the checkbox to checked
        if department.id in user_department_ids:
            checkbox.setChecked(True)

        # Add the checkbox widget to the vbox_departments layout
        vboxDepartments.addWidget(checkbox)


def new_user(main_window) -> None:

    clear_user_entryform(main_window)

    main_window.ui.user_entryform_txtFirstName.setFocus()

    navigate(main_window, Page.USER_ENTRYFORM)


def edit_user(main_window, user_id: int = None) -> None:

    if not user_id:
        user_id = selected_row_id(main_window.ui.user_listingview_tblUser)

    global global_users
    global_users = select_by_attrs_dict(User)
    entity = global_users[user_id]

    clear_user_entryform(main_window, user_id)

    main_window.ui.user_entryform_lblId.setText(str(user_id))
    main_window.ui.user_entryform_txtFirstName.setText(entity.first_name)
    main_window.ui.user_entryform_txtLastName.setText(entity.last_name)
    main_window.ui.user_entryform_txtJobTitle.setText(entity.job_title)
    main_window.ui.user_entryform_txtEmailAddress.setText(entity.email_address)
    main_window.ui.user_entryform_txtUsername.setText(entity.username)
    main_window.ui.user_entryform_txtOldPassword.clear()
    main_window.ui.user_entryform_txtNewPassword.clear()
    main_window.ui.user_entryform_spnPermissionLevel.setValue(entity.permission_level)
    main_window.ui.user_entryform_chkAvailable.setChecked(entity.available)

    user_is_admin = main_window.current_user.permission_level >= 3

    main_window.ui.user_entryform_spnPermissionLevel.setEnabled(user_is_admin)
    main_window.ui.user_entryform_groupDepartments.setEnabled(user_is_admin)

    navigate(main_window, Page.USER_ENTRYFORM)


def delete_user(main_window) -> None:

    if not askyesno(
        "Confirm delete", "Are you sure you would like to delete the selected record?"
    ):
        return

    selected_id = selected_row_id(main_window.ui.user_listingview_tblUser)
    global global_users
    entity = global_users[selected_id]

    delete_by_attrs_dict(User, {"id": entity.id})

    Notification(
        "Delete Successful",
        [f"Successfully deleted user: {entity.first_name} {entity.last_name}"],
    ).show()

    load_user_listingview(main_window)


def user_entryform_is_valid(main_window) -> bool:

    error_strings = list()

    if not main_window.ui.user_entryform_txtFirstName.text():
        error_strings.append("First Name field cannot be blank.")

    if not main_window.ui.user_entryform_txtLastName.text():
        error_strings.append("Last Name field cannot be blank.")

    email_address = main_window.ui.user_entryform_txtEmailAddress.text()
    if not email_address:
        error_strings.append("Email Address field cannot be blank.")
    elif not is_valid_email(email_address):
        error_strings.append("Email Address is not valid.")

    username = main_window.ui.user_entryform_txtUsername.text()
    existing_users = None
    existing_user = None
    if not username:
        error_strings.append("Username field cannot be blank.")
    else:
        existing_users = select_by_attrs_dict(User, {"username": username})
        editing_id = main_window.ui.user_entryform_lblId.text()

        if existing_users and editing_id:

            existing_user = list(existing_users.values())[0]

            if existing_user.id != int(editing_id):
                error_strings.append(f"Username: {username}, already exists.")

    if main_window.current_user.permission_level <= 2:
        old_password = main_window.ui.user_entryform_txtOldPassword.text()
        new_password = main_window.ui.user_entryform_txtNewPassword.text()

        if not old_password:
            error_strings.append("Old Password field cannot be blank.")

        if not new_password:
            error_strings.append("New Password field cannot be blank.")

        if old_password and new_password:
            selected_id = None
            if id_text := main_window.ui.user_entryform_lblId.text():
                all_entities = select_by_attrs_dict(User)
                selected_id = int(id_text)
                selected_entity = all_entities[selected_id]

                if hash_sha512(old_password) != selected_entity.password:
                    error_strings.append("Old Password is not correct.")
            else:
                if old_password != new_password:
                    error_strings.append("Old Password does not match New Password.")

    vboxDepartments = main_window.ui.user_entryform_vboxDepartments
    if not any(
        [
            vboxDepartments.itemAt(i).widget().isChecked()
            for i in range(vboxDepartments.count())
        ]
    ):
        error_strings.append("At least one department must be selected.")

    if error_strings:
        Notification("Cannot Save User", error_strings).show()

    return not bool(error_strings)


def save_and_delete_userdepartments(main_window, entity_id):

    user_departments = select_by_attrs_dict(
        UserDepartment, {"user_id": entity_id}
    ).values()
    department_ids = [ud.department_id for ud in user_departments]

    userdepartments_to_save = list()
    vboxDepartments = main_window.ui.user_entryform_vboxDepartments

    for i in range(vboxDepartments.count()):
        widget = vboxDepartments.itemAt(i).widget()

        if isinstance(widget, QCheckBox):
            department = widget.property("object")

            if widget.isChecked():

                if department.id not in department_ids:
                    userdepartments_to_save.append(
                        UserDepartment(None, entity_id, department.id)
                    )

            else:

                if department.id in department_ids:
                    delete_by_attrs_dict(
                        UserDepartment,
                        {"user_id": entity_id, "department_id": department.id},
                    )

    save_by_list(userdepartments_to_save)


def save_user(main_window) -> None:

    if not user_entryform_is_valid(main_window):
        return

    if not askyesno(
        "Confirm save", "Are you sure you would like to save the current record?"
    ):
        return

    old_password = main_window.ui.user_entryform_txtOldPassword.text()
    new_password = main_window.ui.user_entryform_txtNewPassword.text()

    entity = User(
        None
        if len(main_window.ui.user_entryform_lblId.text()) == 0
        else int(main_window.ui.user_entryform_lblId.text()),
        main_window.ui.user_entryform_txtFirstName.text(),
        main_window.ui.user_entryform_txtLastName.text(),
        main_window.ui.user_entryform_txtJobTitle.text(),
        main_window.ui.user_entryform_txtEmailAddress.text(),
        main_window.ui.user_entryform_txtUsername.text(),
        None,
        main_window.ui.user_entryform_spnPermissionLevel.value(),
        main_window.ui.user_entryform_chkAvailable.isChecked(),
    )

    if not old_password or not new_password:
        if id_text := main_window.ui.user_entryform_lblId.text():
            _id = int(id_text)
            if matches := list(select_by_attrs_dict(User, {"id": _id}).values()):
                match = matches[0]
                entity.password = match.password
    else:
        entity.password = hash_sha512(
            main_window.ui.user_entryform_txtNewPassword.text()
        )

    entity_id = sorted(save_by_list([entity]), key=lambda e: e.id, reverse=True)[0].id

    save_and_delete_userdepartments(main_window, entity_id)

    Notification(
        "Save Successful",
        [f"Successfully saved user: {entity.first_name} {entity.last_name}"],
    ).show()

    load_user_listingview(main_window)

    clear_user_entryform(main_window)


def back_to_user_listingview(main_window) -> None:

    clear_user_entryform(main_window)

    if main_window.current_user.permission_level <= 1:
        navigate(main_window, Page.ASSIGNEE_LISTINGVIEW)
    else:
        navigate(main_window, Page.USER_LISTINGVIEW)


def users_by_search(main_window, search_text: str) -> None:

    global global_users

    if not search_text:
        matches = list(global_users.values())
    else:
        matches = list(
            filter(
                lambda e: search_text
                in "".join(
                    [
                        str(e.id),
                        e.first_name.lower(),
                        e.last_name.lower(),
                        e.job_title.lower(),
                        e.email_address.lower(),
                    ]
                ),
                global_users.values(),
            )
        )

    load_entities_into_table(
        main_window.ui.user_listingview_tblUser,
        matches,
        {
            "id": "ID",
            "first_name": "First Name",
            "last_name": "Last Name",
            "job_title": "Job Title",
            "email_address": "Email Address",
            "permission_level": "Permission Level",
            "available": "Available",
        },
    )


def set_user_button_visibility(main_window):

    if main_window.current_user.permission_level <= 1:
        set_button_visibility(
            [
                main_window.ui.user_listingview_btnNew,
                main_window.ui.user_listingview_btnEdit,
                main_window.ui.user_listingview_btnDelete,
            ],
            is_visible=False,
        )
    else:
        set_button_visibility([main_window.ui.user_listingview_btnNew], is_visible=True)
        set_button_visibility(
            [
                main_window.ui.user_listingview_btnEdit,
                main_window.ui.user_listingview_btnDelete,
            ],
            is_visible=selected_row_id(main_window.ui.user_listingview_tblUser)
            is not None,
        )


def connect_user_actions(main_window) -> None:

    main_window.ui.action_users.triggered.connect(
        lambda: load_user_listingview(main_window)
    )
    main_window.ui.action_logout.triggered.connect(
        lambda: main_window.login_window.log_out_user()
    )
    main_window.ui.action_myaccount.triggered.connect(
        lambda: edit_user(main_window, main_window.current_user.id)
    )
    main_window.ui.user_listingview_btnNew.clicked.connect(
        lambda: new_user(main_window)
    )
    main_window.ui.user_listingview_btnEdit.clicked.connect(
        lambda: edit_user(main_window)
    )
    main_window.ui.user_listingview_btnDelete.clicked.connect(
        lambda: delete_user(main_window)
    )
    main_window.ui.user_entryform_btnSave.clicked.connect(
        lambda: save_user(main_window)
    )
    main_window.ui.user_entryform_btnBack.clicked.connect(
        lambda: back_to_user_listingview(main_window)
    )
    main_window.ui.user_listingview_txtSearch.textChanged.connect(
        lambda: users_by_search(
            main_window, main_window.ui.user_listingview_txtSearch.text().lower()
        )
    )
    main_window.ui.user_listingview_tblUser.itemSelectionChanged.connect(
        lambda: set_user_button_visibility(main_window)
    )
