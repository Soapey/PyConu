from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import QDate
from tkinter.messagebox import askyesno
from datetime import datetime, date
import calendar

from conu.classes.RecurringWorkOrder import RecurringWorkOrder
from conu.classes.UserDepartment import UserDepartment
from conu.classes.RecurringWorkOrderItem import RecurringWorkOrderItem
from conu.classes.Department import Department
from conu.classes.Site import Site
from conu.classes.ItemDepartment import ItemDepartment
from conu.classes.AssigneeDepartment import AssigneeDepartment
from conu.classes.PriorityLevel import PriorityLevel

from conu.classes.User import User
from conu.classes.Item import Item
from conu.classes.Assignee import Assignee

from conu.db.helpers import (
    delete_by_attrs_dict,
    delete_entities_by_ids,
    save_by_list,
    select_by_attrs_dict,
    get_by_user_departments,
)
from conu.helpers import (
    navigate,
    selected_row_id,
    set_button_visibility,
    load_query_rows_into_table,
    load_entities_into_table,
)
from conu.ui.components.Notification import SuccessNotification, ErrorNotification
from conu.ui.components.TableManager import TableManager
from conu.ui.PageEnum import Page
from conu.ui.components.SelectWindow import SelectWindow
from enum import Enum


class SelectionWidgetPage(Enum):

    DAILY = 0
    WEEKLY = 1
    MONTHLY = 2
    YEARLY = 3


unassigned_items_tbl: TableManager = None
assigned_items_tbl: TableManager = None
options = None


def load_recurringworkorder_listingview(main_window) -> None:

    main_window.ui.recurringworkorder_listingview_txtSearch.clear()

    global recurringworkorder_table_data
    recurringworkorder_table_data = RecurringWorkOrder.get_listingview_table_data(
        main_window
    )

    recurringworkorders_by_search(main_window)

    set_recurringworkorder_button_visibility(main_window)

    navigate(main_window, Page.RECURRINGWORKORDER_LISTINGVIEW)


def clear_recurringworkorder_entryform(main_window) -> None:

    main_window.ui.recurringworkorder_entryform_lblId.clear()
    main_window.ui.recurringworkorder_entryform_lblLastRaisedDate.clear()

    main_window.ui.recurringworkorder_entryform_lblSite.clear()
    main_window.ui.recurringworkorder_entryform_lblSite.setProperty("object", None)

    main_window.ui.recurringworkorder_entryform_lblDepartment.clear()
    main_window.ui.recurringworkorder_entryform_lblDepartment.setProperty(
        "object", None
    )

    main_window.ui.recurringworkorder_entryform_lblPriorityLevel.clear()
    main_window.ui.recurringworkorder_entryform_lblPriorityLevel.setProperty(
        "object", None
    )

    main_window.ui.recurringworkorder_entryform_txtTaskDescription.clear()
    main_window.ui.recurringworkorder_entryform_txtComments.clear()

    main_window.ui.recurringworkorder_entryform_dteStartDate.setDate(QDate(2000, 1, 1))

    global unassigned_items_tbl, assigned_items_tbl

    unassigned_items_tbl = TableManager(
        main_window.ui.recurringworkorder_entryform_tblUnassignedItems, ["ID", "Name"]
    )
    assigned_items_tbl = TableManager(
        main_window.ui.recurringworkorder_entryform_tblAssignedItems, ["ID", "Name"]
    )

    unassigned_items_tbl.clear()
    assigned_items_tbl.clear()

    clear_selection_widget(main_window)


def new_recurringworkorder(main_window) -> None:

    clear_recurringworkorder_entryform(main_window)

    load_selection_tables(main_window)

    main_window.ui.recurringworkorder_entryform_txtTaskDescription.setFocus()

    navigate(main_window, Page.RECURRINGWORKORDER_ENTRYFORM)


def get_recurringworkingorder_from_entryform(main_window):

    global options

    selected_option_name = None
    recurringworkorder_type = None

    for option in options.keys():
        if option.isChecked():
            selected_option_name = option.objectName()
            recurringworkorder_type = selected_option_name.split("_")[2]
            break

    selected_option = None
    if "option2" in selected_option_name.lower():
        selected_option = 2
    else:
        selected_option = 1

    recurringworkorder_id = (
        None
        if len(main_window.ui.recurringworkorder_entryform_lblId.text()) == 0
        else int(main_window.ui.recurringworkorder_entryform_lblId.text())
    )

    recurringworkorder_site = (
        main_window.ui.recurringworkorder_entryform_lblSite.property("object")
    )
    recurringworkorder_department = (
        main_window.ui.recurringworkorder_entryform_lblDepartment.property("object")
    )
    recurringworkorder_prioritylevel = (
        main_window.ui.recurringworkorder_entryform_lblPriorityLevel.property("object")
    )
    recurringworkorder_taskdescription = (
        main_window.ui.recurringworkorder_entryform_txtTaskDescription.toPlainText()
    )
    recurringworkorder_comments = (
        None
        if len(main_window.ui.recurringworkorder_entryform_txtComments.toPlainText())
        == 0
        else main_window.ui.recurringworkorder_entryform_txtComments.toPlainText()
    )

    recurringworkorder_start_date_qdate = (
        main_window.ui.recurringworkorder_entryform_dteStartDate.date()
    )
    recurringworkorder_start_date = date(
        recurringworkorder_start_date_qdate.year(),
        recurringworkorder_start_date_qdate.month(),
        recurringworkorder_start_date_qdate.day(),
    )

    recurringworkorder_lastraised_date = (
        recurringworkorder_start_date
        if not recurringworkorder_id
        else datetime.strptime(
            main_window.ui.recurringworkorder_entryform_lblLastRaisedDate.text(),
            "%d-%m-%Y",
        ).date()
    )

    recurringworkorder_interval = None
    recurringworkorder_weekdays = None
    recurringworkorder_day = None
    recurringworkorder_month = None
    recurringworkorder_month_weekday_occurrence = None

    if recurringworkorder_type == "daily":

        if selected_option == 1:
            recurringworkorder_interval = (
                main_window.ui.recurringworkorder_entryform_daily_spnOption1.value()
            )

        elif selected_option == 2:
            recurringworkorder_weekdays = "1;2;3;4;5"

    elif recurringworkorder_type == "weekly":
        recurringworkorder_interval = (
            main_window.ui.recurringworkorder_entryform_weekly_spnOption1.value()
        )

        checked_weekday_indexes = list()

        if (
            main_window.ui.recurringworkorder_entryform_weekly_chkOption1_monday.isChecked()
        ):
            checked_weekday_indexes.append("1")
        if (
            main_window.ui.recurringworkorder_entryform_weekly_chkOption1_tuesday.isChecked()
        ):
            checked_weekday_indexes.append("2")
        if (
            main_window.ui.recurringworkorder_entryform_weekly_chkOption1_wednesday.isChecked()
        ):
            checked_weekday_indexes.append("3")
        if (
            main_window.ui.recurringworkorder_entryform_weekly_chkOption1_thursday.isChecked()
        ):
            checked_weekday_indexes.append("4")
        if (
            main_window.ui.recurringworkorder_entryform_weekly_chkOption1_friday.isChecked()
        ):
            checked_weekday_indexes.append("5")
        if (
            main_window.ui.recurringworkorder_entryform_weekly_chkOption1_saturday.isChecked()
        ):
            checked_weekday_indexes.append("6")
        if (
            main_window.ui.recurringworkorder_entryform_weekly_chkOption1_sunday.isChecked()
        ):
            checked_weekday_indexes.append("7")

        recurringworkorder_weekdays = ";".join(checked_weekday_indexes)

    elif recurringworkorder_type == "monthly":

        if selected_option == 1:
            recurringworkorder_day = (
                main_window.ui.recurringworkorder_entryform_monthly_spnOption1_day.value()
            )
            recurringworkorder_interval = (
                main_window.ui.recurringworkorder_entryform_monthly_spnOption1_month.value()
            )

        elif selected_option == 2:

            occurrence_text = (
                main_window.ui.recurringworkorder_entryform_monthly_cmbOption2_occurrence.currentText()
            )
            if occurrence_text == "first":
                recurringworkorder_month_weekday_occurrence = 1
            elif occurrence_text == "second":
                recurringworkorder_month_weekday_occurrence = 2
            elif occurrence_text == "third":
                recurringworkorder_month_weekday_occurrence = 3
            elif occurrence_text == "last":
                recurringworkorder_month_weekday_occurrence = -1

            recurringworkorder_weekdays = str(
                list(calendar.day_name).index(
                    main_window.ui.recurringworkorder_entryform_cmbOption2_weekday.currentText()
                )
                + 1
            )

            recurringworkorder_interval = (
                main_window.ui.recurringworkorder_entryform_spnOption2.value()
            )

    elif recurringworkorder_type == "yearly":

        if selected_option == 1:
            recurringworkorder_interval = (
                main_window.ui.recurringworkorder_entryform_yearly_spnOption1_year.value()
            )
            recurringworkorder_month = (
                list(calendar.month_name).index(
                    main_window.ui.recurringworkorder_entryform_yearly_cmbOption1.currentText()
                )
                + 1
            )
            recurringworkorder_day = (
                main_window.ui.recurringworkorder_entryform_yearly_spnOption1_day.value()
            )

        elif selected_option == 2:
            recurringworkorder_interval = (
                main_window.ui.recurringworkorder_entryform_yearly_spnOption2.value()
            )

            occurrence_text = (
                main_window.ui.recurringworkorder_entryform_yearly_cmbOption2_occurrence.currentText()
            )
            if occurrence_text == "first":
                recurringworkorder_month_weekday_occurrence = 1
            elif occurrence_text == "second":
                recurringworkorder_month_weekday_occurrence = 2
            elif occurrence_text == "third":
                recurringworkorder_month_weekday_occurrence = 3
            elif occurrence_text == "last":
                recurringworkorder_month_weekday_occurrence = -1

            recurringworkorder_weekdays = str(
                list(calendar.day_name).index(
                    main_window.ui.recurringworkorder_entryform_yearly_cmbOption2_weekday.currentText()
                )
                + 1
            )

            recurringworkorder_month = (
                list(calendar.month_name).index(
                    main_window.ui.recurringworkorder_entryform_yearly_cmbOption2_month.currentText()
                )
                + 1
            )

    return RecurringWorkOrder(
        recurringworkorder_id,
        recurringworkorder_site.id,
        recurringworkorder_department.id,
        recurringworkorder_prioritylevel.id,
        recurringworkorder_taskdescription,
        recurringworkorder_comments,
        recurringworkorder_type,
        recurringworkorder_start_date,
        recurringworkorder_lastraised_date,
        recurringworkorder_interval,
        recurringworkorder_weekdays,
        recurringworkorder_day,
        recurringworkorder_month,
        recurringworkorder_month_weekday_occurrence,
    )


def load_recurrence_selection_widget(
    main_window, recurringworkorder: RecurringWorkOrder
):

    weekday_occurrences = {1: "first", 2: "second", 3: "third", -1: "last"}

    if recurringworkorder.weekdays:
        weekdays = [
            calendar.day_name[int(wd) - 1].lower()
            for wd in recurringworkorder.weekdays.split(";")
        ]

    if recurringworkorder.type == "daily":

        if recurringworkorder.interval:
            main_window.ui.recurringworkorder_entryform_daily_radOption1.setChecked(
                True
            )
            main_window.ui.recurringworkorder_entryform_daily_spnOption1.setValue(
                recurringworkorder.interval
            )
            select_option(main_window.ui.recurringworkorder_entryform_daily_radOption1)

        elif recurringworkorder.weekdays:
            main_window.ui.recurringworkorder_entryform_daily_radOption2.setChecked(
                True
            )
            select_option(main_window.ui.recurringworkorder_entryform_daily_radOption2)

        main_window.ui.recurringworkorder_entryform_radDaily.setChecked(True)

    elif recurringworkorder.type == "weekly" and recurringworkorder.weekdays:

        main_window.ui.recurringworkorder_entryform_weekly_radOption1.setChecked(True)
        main_window.ui.recurringworkorder_entryform_weekly_spnOption1.setValue(
            recurringworkorder.interval
        )

        all_lowered_weekday_names = [calendar.day_name[i].lower() for i in range(7)]

        for weekday_name in all_lowered_weekday_names:
            weekday_checkbox = main_window.ui.recurringworkorder_entryform_weekly_groupOption1.findChild(
                QCheckBox,
                f"recurringworkorder_entryform_weekly_chkOption1_{weekday_name}",
            )

            if weekday_name in weekdays:
                weekday_checkbox.setChecked(True)
            else:
                weekday_checkbox.setChecked(False)

        select_option(main_window.ui.recurringworkorder_entryform_weekly_radOption1)

        main_window.ui.recurringworkorder_entryform_radWeekly.setChecked(True)

    elif recurringworkorder.type == "monthly":

        if recurringworkorder.day and recurringworkorder.interval:

            main_window.ui.recurringworkorder_entryform_monthly_radOption1.setChecked(
                True
            )
            main_window.ui.recurringworkorder_entryform_monthly_spnOption1_day.setValue(
                recurringworkorder.day
            )
            main_window.ui.recurringworkorder_entryform_monthly_spnOption1_month.setValue(
                recurringworkorder.interval
            )
            select_option(
                main_window.ui.recurringworkorder_entryform_monthly_radOption1
            )

        elif (
            recurringworkorder.month_weekday_occurrence
            and recurringworkorder.weekdays
            and recurringworkorder.interval
        ):

            main_window.ui.recurringworkorder_entryform_monthly_radOption2.setChecked(
                True
            )
            main_window.ui.recurringworkorder_entryform_monthly_cmbOption2_occurrence.setCurrentText(
                weekday_occurrences[recurringworkorder.month_weekday_occurrence]
            )
            main_window.ui.recurringworkorder_entryform_cmbOption2_weekday.setCurrentText(
                weekdays[0].title()
            )
            main_window.ui.recurringworkorder_entryform_spnOption2.setValue(
                recurringworkorder.interval
            )
            select_option(
                main_window.ui.recurringworkorder_entryform_monthly_radOption2
            )

        main_window.ui.recurringworkorder_entryform_radMonthly.setChecked(True)

    elif recurringworkorder.type == "yearly":

        if recurringworkorder.month and recurringworkorder.day:

            main_window.ui.recurringworkorder_entryform_yearly_radOption1.setChecked(
                True
            )
            main_window.ui.recurringworkorder_entryform_yearly_spnOption1_year.setValue(
                recurringworkorder.interval
            )
            main_window.ui.recurringworkorder_entryform_yearly_cmbOption1.setCurrentText(
                calendar.month_name[recurringworkorder.month]
            )
            main_window.ui.recurringworkorder_entryform_yearly_spnOption1_day.setValue(
                recurringworkorder.day
            )
            select_option(main_window.ui.recurringworkorder_entryform_yearly_radOption1)

        elif (
            recurringworkorder.month_weekday_occurrence
            and recurringworkorder.weekdays
            and recurringworkorder.month
        ):

            main_window.ui.recurringworkorder_entryform_yearly_radOption2.setChecked(
                True
            )
            main_window.ui.recurringworkorder_entryform_yearly_spnOption2.setValue(
                recurringworkorder.interval
            )
            main_window.ui.recurringworkorder_entryform_yearly_cmbOption2_occurrence(
                weekday_occurrences[recurringworkorder.month_weekday_occurrence]
            )
            main_window.ui.recurringworkorder_entryform_yearly_cmbOption2_weekday.setCurrentText(
                weekdays[0].title()
            )
            main_window.ui.recurringworkorder_entryform_yearly_cmbOption2_month.setCurrentText(
                calendar.month_name[recurringworkorder.month]
            )
            select_option(main_window.ui.recurringworkorder_entryform_yearly_radOption2)

        main_window.ui.recurringworkorder_entryform_radYearly.setChecked(True)


def edit_recurringworkorder(main_window, entity_id=None) -> None:

    sites = select_by_attrs_dict(Site)
    departments = select_by_attrs_dict(Department)
    prioritylevels = select_by_attrs_dict(PriorityLevel)

    if not entity_id:
        entity_id = selected_row_id(
            main_window.ui.recurringworkorder_listingview_tblRecurringWorkOrder
        )
    recurringworkorders = RecurringWorkOrder.get()
    entity = recurringworkorders[entity_id]

    recurringworkorder_site = sites[entity.site_id]
    recurringworkorder_department = departments[entity.department_id]
    recurringworkorder_prioritylevel = prioritylevels[entity.prioritylevel_id]

    clear_recurringworkorder_entryform(main_window)

    main_window.ui.recurringworkorder_entryform_lblId.setText(str(entity.id))

    main_window.ui.recurringworkorder_entryform_lblLastRaisedDate.setText(
        datetime.strftime(entity.lastraised_date, "%d-%m-%Y")
    )

    main_window.ui.recurringworkorder_entryform_lblSite.setProperty(
        "object", recurringworkorder_site
    )
    main_window.ui.recurringworkorder_entryform_lblSite.setText(
        recurringworkorder_site.name
    )

    main_window.ui.recurringworkorder_entryform_lblDepartment.setProperty(
        "object", recurringworkorder_department
    )
    main_window.ui.recurringworkorder_entryform_lblDepartment.setText(
        recurringworkorder_department.name
    )

    main_window.ui.recurringworkorder_entryform_lblPriorityLevel.setProperty(
        "object", recurringworkorder_prioritylevel
    )
    main_window.ui.recurringworkorder_entryform_lblPriorityLevel.setText(
        recurringworkorder_prioritylevel.name
    )

    main_window.ui.recurringworkorder_entryform_txtTaskDescription.setPlainText(
        entity.task_description
    )

    if comments := entity.comments:
        main_window.ui.recurringworkorder_entryform_txtComments.setPlainText(comments)

    start_date = entity.start_date
    main_window.ui.recurringworkorder_entryform_dteStartDate.setDate(
        QDate(start_date.year, start_date.month, start_date.day)
    )

    load_selection_tables(main_window)

    load_recurrence_selection_widget(main_window, entity)

    main_window.ui.recurringworkorder_entryform_txtTaskDescription.setFocus()

    navigate(main_window, Page.RECURRINGWORKORDER_ENTRYFORM)


def delete_recurringworkorder(main_window) -> None:

    if not askyesno(
        "Confirm delete", "Are you sure you would like to delete the selected record?"
    ):
        return

    selected_id = selected_row_id(
        main_window.ui.recurringworkorder_listingview_tblRecurringWorkOrder
    )

    recurringworkorders = RecurringWorkOrder.get()
    entity = recurringworkorders[selected_id]

    if not entity:
        return

    delete_entities_by_ids(RecurringWorkOrder, [selected_id])

    SuccessNotification(
        "Delete Successful",
        [f"Successfully deleted recurring work order: {selected_id}"],
    ).show()

    load_recurringworkorder_listingview(main_window)


def export_recurringworkorder_table(main_window):

    RecurringWorkOrder.get_listingview_table_data(main_window, export_to_excel=True)

def recurringworkorder_entryform_is_valid(main_window) -> bool:

    error_strings = list()

    if not main_window.ui.recurringworkorder_entryform_lblSite.text():
        error_strings.append("A site must be selected.")

    if not main_window.ui.recurringworkorder_entryform_lblDepartment.text():
        error_strings.append("A department must be selected.")

    if not main_window.ui.recurringworkorder_entryform_lblPriorityLevel.text():
        error_strings.append("A priority level must be selected.")

    if not main_window.ui.recurringworkorder_entryform_tblAssignedItems.rowCount() >= 1:
        error_strings.append("At least one item must be assigned.")

    if not main_window.ui.recurringworkorder_entryform_txtTaskDescription.toPlainText():
        error_strings.append("Task Description field cannot be blank.")

    global options

    selected_option_name = None
    recurringworkorder_type = None

    for option in options.keys():
        if option.isChecked():
            selected_option_name = option.objectName()
            recurringworkorder_type = selected_option_name.split("_")[2]
            break

    selected_option = None
    if "option2" in selected_option_name.lower():
        selected_option = 2
    else:
        selected_option = 1

    if recurringworkorder_type == "weekly":

        if not any(
            [
                main_window.ui.recurringworkorder_entryform_weekly_chkOption1_monday.isChecked(),
                main_window.ui.recurringworkorder_entryform_weekly_chkOption1_tuesday.isChecked(),
                main_window.ui.recurringworkorder_entryform_weekly_chkOption1_wednesday.isChecked(),
                main_window.ui.recurringworkorder_entryform_weekly_chkOption1_thursday.isChecked(),
                main_window.ui.recurringworkorder_entryform_weekly_chkOption1_friday.isChecked(),
                main_window.ui.recurringworkorder_entryform_weekly_chkOption1_saturday.isChecked(),
                main_window.ui.recurringworkorder_entryform_weekly_chkOption1_sunday.isChecked(),
            ]
        ):
            error_strings.append(
                "At least weekday for a weekly recurrence must be selected."
            )

    elif recurringworkorder_type == "monthly":

        if selected_option == 2:

            if (
                len(
                    main_window.ui.recurringworkorder_entryform_monthly_cmbOption2_occurrence.currentText()
                )
                == 0
                or len(
                    main_window.ui.recurringworkorder_entryform_cmbOption2_weekday.currentText()
                )
                == 0
            ):
                error_strings.append(
                    "All fields must be filled out for the selected monthly recurrence option."
                )

    elif recurringworkorder_type == "yearly":

        if selected_option == 1:

            if (
                len(
                    main_window.ui.recurringworkorder_entryform_yearly_cmbOption1.currentText()
                )
                == 0
            ):
                error_strings.append(
                    "All fields must be filled out for the selected yearly recurrence option."
                )

        elif selected_option == 2:

            if (
                len(
                    main_window.ui.recurringworkorder_entryform_yearly_cmbOption2_occurrence.currentText()
                )
                == 0
                or len(
                    main_window.ui.recurringworkorder_entryform_yearly_cmbOption2_weekday.currentText()
                )
                == 0
                or len(
                    main_window.ui.recurringworkorder_entryform_yearly_cmbOption2_month.currentText()
                )
                == 0
            ):
                error_strings.append(
                    "All fields must be filled out for the selected yearly recurrence option."
                )

    if error_strings:
        ErrorNotification("Cannot Save Recurring Work Order", error_strings).show()

    return not bool(error_strings)


def save_and_delete_recurringworkorderitems(main_window, entity_id):

    existing_item_ids = [
        rwoi.item_id
        for rwoi in select_by_attrs_dict(
            RecurringWorkOrderItem, {"recurringworkorder_id": entity_id}
        ).values()
    ]

    assigned_item_ids = list()
    recurringworkorderitems_to_save = list()

    tbl = main_window.ui.recurringworkorder_entryform_tblAssignedItems
    id_column_index = 0

    for row_index in range(tbl.rowCount()):
        _cell = tbl.item(row_index, id_column_index)
        _id = int(_cell.text())
        assigned_item_ids.append(_id)

        if _id not in list(existing_item_ids):
            recurringworkorderitems_to_save.append(
                RecurringWorkOrderItem(None, entity_id, _id)
            )

    for item_id in existing_item_ids:
        if item_id not in assigned_item_ids:
            delete_by_attrs_dict(
                RecurringWorkOrderItem,
                {"recurringworkorder_id": entity_id, "item_id": item_id},
            )

    save_by_list(recurringworkorderitems_to_save)


def save_recurringworkorder(main_window) -> None:

    if not recurringworkorder_entryform_is_valid(main_window):
        return

    if not askyesno(
        "Confirm save", "Are you sure you would like to save the current record?"
    ):
        return

    entity = get_recurringworkingorder_from_entryform(main_window)

    entity_id = sorted(save_by_list([entity]), key=lambda e: e.id, reverse=True)[0].id

    save_and_delete_recurringworkorderitems(main_window, entity_id)

    SuccessNotification(
        "Save Successful", [f"Successfully saved recurring work order: {entity_id}"]
    ).show()

    load_recurringworkorder_listingview(main_window)

    clear_recurringworkorder_entryform(main_window)


def back_to_recurringworkorder_listingview(main_window) -> None:

    clear_recurringworkorder_entryform(main_window)

    navigate(main_window, Page.RECURRINGWORKORDER_LISTINGVIEW)


def recurringworkorders_by_search(main_window) -> None:

    search_text = main_window.ui.recurringworkorder_listingview_txtSearch.text().lower()

    global recurringworkorder_table_data

    if not search_text:
        matches = recurringworkorder_table_data
    else:
        print("recurringworkorders_by_search called.")

        matches = list(
            filter(
                lambda tup: search_text
                in "".join(
                    [
                        str(tup[0]),
                        str(tup[1]),
                        str(tup[2]),
                        str(tup[4]),
                        str(tup[5]),
                        str(tup[7]),
                    ]
                ).lower(),
                recurringworkorder_table_data,
            )
        )

    load_query_rows_into_table(
        main_window.ui.recurringworkorder_listingview_tblRecurringWorkOrder,
        matches,
        {
            "ID": (0, str),
            "Site": (1, None),
            "Department": (2, None),
            "Priority Level": (3, None),
            "Task Description": (4, None),
            "Comments": (5, None),
            "Recurrence": (6, None),
            "Due": (7, str),
        },
    )


def set_recurringworkorder_button_visibility(main_window):

    if main_window.current_user.permission_level <= 1:
        set_button_visibility(
            [
                main_window.ui.recurringworkorder_listingview_btnNew,
                main_window.ui.recurringworkorder_listingview_btnEdit,
                main_window.ui.recurringworkorder_listingview_btnDelete,
            ],
            is_visible=False,
        )
    else:
        set_button_visibility(
            [main_window.ui.recurringworkorder_listingview_btnNew], is_visible=True
        )
        set_button_visibility(
            [
                main_window.ui.recurringworkorder_listingview_btnEdit,
                main_window.ui.recurringworkorder_listingview_btnDelete,
            ],
            is_visible=selected_row_id(
                main_window.ui.recurringworkorder_listingview_tblRecurringWorkOrder
            )
            is not None,
        )


def transfer_item_to_table(from_table: TableManager, to_table: TableManager):

    selected_item = from_table.first_selected_item()

    if not selected_item:
        return

    selected_row = selected_item.row()
    selected_id = int(selected_item.text())

    items = select_by_attrs_dict(Item)
    selected_entity = items[selected_id]

    from_table.remove_row(selected_row)

    to_table.add_row()

    to_table.set_item(to_table.last_row_index, 0, str(selected_id))
    to_table.set_item(to_table.last_row_index, 1, selected_entity.name)


def select_site(main_window):

    sites = select_by_attrs_dict(Site)

    SelectWindow(
        sites,
        main_window.ui.recurringworkorder_entryform_lblSite.setText,
        "name",
        main_window.ui.recurringworkorder_entryform_lblSite.setProperty,
        {"id": "ID", "name": "Name"},
    )


def select_department(main_window):

    departments = main_window.current_user.get_departments()

    SelectWindow(
        departments,
        main_window.ui.recurringworkorder_entryform_lblDepartment.setText,
        "name",
        main_window.ui.recurringworkorder_entryform_lblDepartment.setProperty,
        {"id": "ID", "name": "Name"},
        lambda: load_selection_tables(main_window),
    )


def select_prioritylevel(main_window):

    prioritylevels = select_by_attrs_dict(PriorityLevel)

    SelectWindow(
        prioritylevels,
        main_window.ui.recurringworkorder_entryform_lblPriorityLevel.setText,
        "name",
        main_window.ui.recurringworkorder_entryform_lblPriorityLevel.setProperty,
        {"id": "ID", "name": "Name", "days_until_overdue": "Days Until Overdue"},
    )


def load_item_selection_table(main_window):

    id = main_window.ui.recurringworkorder_entryform_lblId.text()

    department = main_window.ui.recurringworkorder_entryform_lblDepartment.property(
        "object"
    )

    global unassigned_items_tbl, assigned_items_tbl
    unassigned_items_tbl.clear()
    assigned_items_tbl.clear()

    if department is None:
        return

    all_items = select_by_attrs_dict(Item)

    item_departments = select_by_attrs_dict(
        ItemDepartment, {"department_id": department.id}
    ).values()

    items = [all_items[item_id] for item_id in {id.item_id for id in item_departments}]

    items = sorted(items, key=lambda e: e.name)

    if id is None or len(id) == 0:
        load_entities_into_table(
            unassigned_items_tbl.table, items, {"id": "ID", "name": "Name"}
        )
        return

    id = int(id)

    recurringworkorder_items = select_by_attrs_dict(
        RecurringWorkOrderItem, {"recurringworkorder_id": id}
    )
    assigned_item_ids = [rwoi.item_id for rwoi in recurringworkorder_items.values()]

    unassigned_items = [item for item in items if item.id not in assigned_item_ids]
    assigned_items = [all_items[item_id] for item_id in assigned_item_ids]

    load_entities_into_table(
        unassigned_items_tbl.table, unassigned_items, {"id": "ID", "name": "Name"}
    )
    load_entities_into_table(
        assigned_items_tbl.table, assigned_items, {"id": "ID", "name": "Name"}
    )


def load_selection_tables(main_window):

    load_item_selection_table(main_window)


def clear_selection_widget(main_window):

    # Daily
    ##### Option 1
    main_window.ui.recurringworkorder_entryform_daily_radOption1.setChecked(False)
    main_window.ui.recurringworkorder_entryform_daily_spnOption1.setValue(1)
    ##### Option 2
    main_window.ui.recurringworkorder_entryform_daily_radOption2.setChecked(False)

    # Weekly
    ##### Option 1
    main_window.ui.recurringworkorder_entryform_weekly_radOption1.setChecked(False)
    main_window.ui.recurringworkorder_entryform_weekly_spnOption1.setValue(1)
    main_window.ui.recurringworkorder_entryform_weekly_chkOption1_monday.setChecked(
        False
    )
    main_window.ui.recurringworkorder_entryform_weekly_chkOption1_tuesday.setChecked(
        False
    )
    main_window.ui.recurringworkorder_entryform_weekly_chkOption1_wednesday.setChecked(
        False
    )
    main_window.ui.recurringworkorder_entryform_weekly_chkOption1_thursday.setChecked(
        False
    )
    main_window.ui.recurringworkorder_entryform_weekly_chkOption1_friday.setChecked(
        False
    )
    main_window.ui.recurringworkorder_entryform_weekly_chkOption1_saturday.setChecked(
        False
    )
    main_window.ui.recurringworkorder_entryform_weekly_chkOption1_sunday.setChecked(
        False
    )

    # Monthly
    ##### Option 1
    main_window.ui.recurringworkorder_entryform_monthly_radOption1.setChecked(False)
    main_window.ui.recurringworkorder_entryform_monthly_spnOption1_day.setValue(1)
    main_window.ui.recurringworkorder_entryform_monthly_spnOption1_month.setValue(1)
    ##### Option 2
    main_window.ui.recurringworkorder_entryform_monthly_radOption2.setChecked(False)
    monthly_cmbOption2_occurrence = (
        main_window.ui.recurringworkorder_entryform_monthly_cmbOption2_occurrence
    )
    monthly_cmbOption2_occurrence.clear()
    monthly_cmbOption2_occurrence.addItem("first")
    monthly_cmbOption2_occurrence.addItem("second")
    monthly_cmbOption2_occurrence.addItem("third")
    monthly_cmbOption2_occurrence.addItem("last")
    monthly_cmbOption2_occurrence.setCurrentIndex(0)
    monthly_cmbOption2_weekday = (
        main_window.ui.recurringworkorder_entryform_cmbOption2_weekday
    )
    monthly_cmbOption2_weekday.clear()
    monthly_cmbOption2_weekday.addItem("Monday")
    monthly_cmbOption2_weekday.addItem("Tuesday")
    monthly_cmbOption2_weekday.addItem("Wednesday")
    monthly_cmbOption2_weekday.addItem("Thursday")
    monthly_cmbOption2_weekday.addItem("Friday")
    monthly_cmbOption2_weekday.addItem("Saturday")
    monthly_cmbOption2_weekday.addItem("Sunday")
    monthly_cmbOption2_weekday.setCurrentIndex(0)
    main_window.ui.recurringworkorder_entryform_spnOption2.setValue(1)

    # Yearly
    ##### Option 1
    main_window.ui.recurringworkorder_entryform_yearly_radOption1.setChecked(False)
    main_window.ui.recurringworkorder_entryform_yearly_spnOption1_year.setValue(1)
    yearly_cmbOption1 = main_window.ui.recurringworkorder_entryform_yearly_cmbOption1
    yearly_cmbOption1.clear()
    yearly_cmbOption1.addItem("January")
    yearly_cmbOption1.addItem("February")
    yearly_cmbOption1.addItem("March")
    yearly_cmbOption1.addItem("April")
    yearly_cmbOption1.addItem("May")
    yearly_cmbOption1.addItem("June")
    yearly_cmbOption1.addItem("July")
    yearly_cmbOption1.addItem("August")
    yearly_cmbOption1.addItem("September")
    yearly_cmbOption1.addItem("October")
    yearly_cmbOption1.addItem("November")
    yearly_cmbOption1.addItem("December")
    yearly_cmbOption1.setCurrentIndex(0)
    ##### Option 2
    main_window.ui.recurringworkorder_entryform_yearly_radOption2.setChecked(False)
    main_window.ui.recurringworkorder_entryform_yearly_spnOption2.setValue(1)
    yearly_cmbOption2_occurence = (
        main_window.ui.recurringworkorder_entryform_yearly_cmbOption2_occurrence
    )
    yearly_cmbOption2_occurence.clear()
    yearly_cmbOption2_occurence.addItem("first")
    yearly_cmbOption2_occurence.addItem("second")
    yearly_cmbOption2_occurence.addItem("third")
    yearly_cmbOption2_occurence.addItem("last")
    yearly_cmbOption2_occurence.setCurrentIndex(0)
    yearly_cmbOption2_weekday = (
        main_window.ui.recurringworkorder_entryform_yearly_cmbOption2_weekday
    )
    yearly_cmbOption2_weekday.clear()
    yearly_cmbOption2_weekday.addItem("Monday")
    yearly_cmbOption2_weekday.addItem("Tuesday")
    yearly_cmbOption2_weekday.addItem("Wednesday")
    yearly_cmbOption2_weekday.addItem("Thursday")
    yearly_cmbOption2_weekday.addItem("Friday")
    yearly_cmbOption2_weekday.addItem("Saturday")
    yearly_cmbOption2_weekday.addItem("Sunday")
    yearly_cmbOption2_weekday.setCurrentIndex(0)
    yearly_cmbOption2_month = (
        main_window.ui.recurringworkorder_entryform_yearly_cmbOption2_month
    )
    yearly_cmbOption2_month.clear()
    yearly_cmbOption2_month.addItem("January")
    yearly_cmbOption2_month.addItem("February")
    yearly_cmbOption2_month.addItem("March")
    yearly_cmbOption2_month.addItem("April")
    yearly_cmbOption2_month.addItem("May")
    yearly_cmbOption2_month.addItem("June")
    yearly_cmbOption2_month.addItem("July")
    yearly_cmbOption2_month.addItem("August")
    yearly_cmbOption2_month.addItem("September")
    yearly_cmbOption2_month.addItem("October")
    yearly_cmbOption2_month.addItem("November")
    yearly_cmbOption2_month.addItem("December")
    yearly_cmbOption2_month.setCurrentIndex(0)

    # Page Selection
    main_window.ui.recurringworkorder_entryform_radDaily.setChecked(True)
    main_window.ui.recurringworkorder_entryform_page_handler.setCurrentIndex(
        SelectionWidgetPage.DAILY.value
    )


def select_option(option_radiobutton):

    if not option_radiobutton.isChecked():
        return

    global options

    for option, children_widgets in options.items():

        if option != option_radiobutton:

            option.setChecked(False)

            for child_widget in children_widgets:
                child_widget.setEnabled(False)

        else:

            option.setChecked(True)

            for child_widget in children_widgets:
                child_widget.setEnabled(True)


def navigate_recurrence_selection_widget(
    main_window, page_selection_radiobutton, selection_widget_page
):

    if not page_selection_radiobutton.isChecked():
        return

    main_window.ui.recurringworkorder_entryform_page_handler.setCurrentIndex(
        selection_widget_page.value
    )


def connect_recurringworkorder_actions(main_window) -> None:

    global unassigned_items_tbl, assigned_items_tbl

    main_window.ui.action_recurringworkorders.triggered.connect(
        lambda: load_recurringworkorder_listingview(main_window)
    )
    main_window.ui.recurringworkorder_listingview_btnNew.clicked.connect(
        lambda: new_recurringworkorder(main_window)
    )
    main_window.ui.recurringworkorder_listingview_btnEdit.clicked.connect(
        lambda: edit_recurringworkorder(main_window)
    )
    main_window.ui.recurringworkorder_listingview_btnDelete.clicked.connect(
        lambda: delete_recurringworkorder(main_window)
    )
    main_window.ui.recurringworkorder_listingview_btnExportTable.clicked.connect(
        lambda: export_recurringworkorder_table(main_window)
    )
    main_window.ui.recurringworkorder_entryform_btnSave.clicked.connect(
        lambda: save_recurringworkorder(main_window)
    )
    main_window.ui.recurringworkorder_entryform_btnBack.clicked.connect(
        lambda: back_to_recurringworkorder_listingview(main_window)
    )
    main_window.ui.recurringworkorder_entryform_btnSelectSite.clicked.connect(
        lambda: select_site(main_window)
    )
    main_window.ui.recurringworkorder_entryform_btnSelectDepartment.clicked.connect(
        lambda: select_department(main_window)
    )
    main_window.ui.recurringworkorder_entryform_btnSelectPriorityLevel.clicked.connect(
        lambda: select_prioritylevel(main_window)
    )
    main_window.ui.recurringworkorder_entryform_btnAssignItemToRecurringWorkOrder.clicked.connect(
        lambda: transfer_item_to_table(unassigned_items_tbl, assigned_items_tbl)
    )
    main_window.ui.recurringworkorder_entryform_btnUnassignItemFromRecurringWorkOrder.clicked.connect(
        lambda: transfer_item_to_table(assigned_items_tbl, unassigned_items_tbl)
    )
    main_window.ui.recurringworkorder_listingview_txtSearch.textChanged.connect(
        lambda: recurringworkorders_by_search(main_window)
    )
    main_window.ui.recurringworkorder_listingview_tblRecurringWorkOrder.itemSelectionChanged.connect(
        lambda: set_recurringworkorder_button_visibility(main_window)
    )

    global options
    options = {
        main_window.ui.recurringworkorder_entryform_daily_radOption1: [
            main_window.ui.recurringworkorder_entryform_daily_spnOption1
        ],
        main_window.ui.recurringworkorder_entryform_daily_radOption2: list(),
        main_window.ui.recurringworkorder_entryform_weekly_radOption1: [
            main_window.ui.recurringworkorder_entryform_weekly_spnOption1,
            main_window.ui.recurringworkorder_entryform_weekly_chkOption1_monday,
            main_window.ui.recurringworkorder_entryform_weekly_chkOption1_tuesday,
            main_window.ui.recurringworkorder_entryform_weekly_chkOption1_wednesday,
            main_window.ui.recurringworkorder_entryform_weekly_chkOption1_thursday,
            main_window.ui.recurringworkorder_entryform_weekly_chkOption1_friday,
            main_window.ui.recurringworkorder_entryform_weekly_chkOption1_saturday,
            main_window.ui.recurringworkorder_entryform_weekly_chkOption1_sunday,
        ],
        main_window.ui.recurringworkorder_entryform_monthly_radOption1: [
            main_window.ui.recurringworkorder_entryform_monthly_spnOption1_day,
            main_window.ui.recurringworkorder_entryform_monthly_spnOption1_month,
        ],
        main_window.ui.recurringworkorder_entryform_monthly_radOption2: [
            main_window.ui.recurringworkorder_entryform_monthly_cmbOption2_occurrence,
            main_window.ui.recurringworkorder_entryform_cmbOption2_weekday,
            main_window.ui.recurringworkorder_entryform_spnOption2,
        ],
        main_window.ui.recurringworkorder_entryform_yearly_radOption1: [
            main_window.ui.recurringworkorder_entryform_yearly_spnOption1_year,
            main_window.ui.recurringworkorder_entryform_yearly_cmbOption1,
            main_window.ui.recurringworkorder_entryform_yearly_spnOption1_day,
        ],
        main_window.ui.recurringworkorder_entryform_yearly_radOption2: [
            main_window.ui.recurringworkorder_entryform_yearly_spnOption2,
            main_window.ui.recurringworkorder_entryform_yearly_cmbOption2_occurrence,
            main_window.ui.recurringworkorder_entryform_yearly_cmbOption2_weekday,
            main_window.ui.recurringworkorder_entryform_yearly_cmbOption2_month,
        ],
    }

    main_window.ui.recurringworkorder_entryform_daily_radOption1.toggled.connect(
        lambda: select_option(
            main_window.ui.recurringworkorder_entryform_daily_radOption1
        )
    )
    main_window.ui.recurringworkorder_entryform_daily_radOption2.toggled.connect(
        lambda: select_option(
            main_window.ui.recurringworkorder_entryform_daily_radOption2
        )
    )
    main_window.ui.recurringworkorder_entryform_weekly_radOption1.toggled.connect(
        lambda: select_option(
            main_window.ui.recurringworkorder_entryform_weekly_radOption1
        )
    )
    main_window.ui.recurringworkorder_entryform_monthly_radOption1.toggled.connect(
        lambda: select_option(
            main_window.ui.recurringworkorder_entryform_monthly_radOption1
        )
    )
    main_window.ui.recurringworkorder_entryform_monthly_radOption2.toggled.connect(
        lambda: select_option(
            main_window.ui.recurringworkorder_entryform_monthly_radOption2
        )
    )
    main_window.ui.recurringworkorder_entryform_yearly_radOption1.toggled.connect(
        lambda: select_option(
            main_window.ui.recurringworkorder_entryform_yearly_radOption1
        )
    )
    main_window.ui.recurringworkorder_entryform_yearly_radOption2.toggled.connect(
        lambda: select_option(
            main_window.ui.recurringworkorder_entryform_yearly_radOption2
        )
    )

    main_window.ui.recurringworkorder_entryform_radDaily.toggled.connect(
        lambda: navigate_recurrence_selection_widget(
            main_window,
            main_window.ui.recurringworkorder_entryform_radDaily,
            SelectionWidgetPage.DAILY,
        )
    )
    main_window.ui.recurringworkorder_entryform_radWeekly.toggled.connect(
        lambda: navigate_recurrence_selection_widget(
            main_window,
            main_window.ui.recurringworkorder_entryform_radWeekly,
            SelectionWidgetPage.WEEKLY,
        )
    )
    main_window.ui.recurringworkorder_entryform_radMonthly.toggled.connect(
        lambda: navigate_recurrence_selection_widget(
            main_window,
            main_window.ui.recurringworkorder_entryform_radMonthly,
            SelectionWidgetPage.MONTHLY,
        )
    )
    main_window.ui.recurringworkorder_entryform_radYearly.toggled.connect(
        lambda: navigate_recurrence_selection_widget(
            main_window,
            main_window.ui.recurringworkorder_entryform_radYearly,
            SelectionWidgetPage.YEARLY,
        )
    )
