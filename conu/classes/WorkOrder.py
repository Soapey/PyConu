from datetime import datetime, date
from conu.db.SQLiteConnection import SQLiteConnection, select_by_attrs_dict
from conu.classes.PriorityLevel import PriorityLevel
from PyQt5.QtWidgets import QTableWidgetItem


class WorkOrder:
    def __init__(
        self,
        id: int,
        site_id: int,
        department_id: int,
        prioritylevel_id: int,
        task_description: str,
        comments: str,
        date_created: date,
        date_allocated: date,
        raisedby_user_id: int,
        date_completed: date,
        purchase_order_number: str,
        close_out_comments: str,
    ) -> None:
        self.id = id
        self.site_id = site_id
        self.department_id = department_id
        self.prioritylevel_id = prioritylevel_id
        self.task_description = task_description
        self.comments = comments
        self.date_created = date_created
        self.date_allocated = date_allocated
        self.raisedby_user_id = raisedby_user_id
        self.date_completed = date_completed
        self.purchase_order_number = purchase_order_number
        self.close_out_comments = close_out_comments

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

    def __str__(self) -> str:
        return self.__repr__()

    def is_due(self, priority_levels: list = None) -> bool:

        if not priority_levels:
            global global_prioritylevels
            if (
                not global_prioritylevels
                or self.prioritylevel_id not in global_prioritylevels
            ):
                global_prioritylevels = select_by_attrs_dict(PriorityLevel)

            priority_levels = global_prioritylevels

        priority_level = priority_levels[self.prioritylevel_id]

        days_until_overdue = priority_level.days_until_overdue

        return (
            not self.date_completed
            and (date.today() - self.date_allocated).days >= days_until_overdue
        )

    @classmethod
    def load_listingview_table_contents(cls, main_window):

        current_user = main_window.current_user

        if not current_user:
            return

        with SQLiteConnection() as cur:
            rows = cur.execute(
                """
            SELECT
                workorder.id,
                site.name,
                department.name,
                prioritylevel.name,
                workorder.task_description,
                GROUP_CONCAT(item.name, ', '),
                GROUP_CONCAT(assignee.name, ', '),
                workorder.comments,
                workorder.date_allocated,
                workorder.date_completed,
                workorder.close_out_comments,
                CONCAT(user.first_name, ' ', user.last_name),
                workorder.date_created
            FROM
                workorder
                JOIN site ON workorder.site_id = site.id
                JOIN department ON workorder.department_id = department.id
                JOIN prioritylevel ON workorder.prioritylevel_id = prioritylevel.id
                JOIN user ON workorder.raisedby_user_id = user.id
                LEFT JOIN workorderitem ON workorder.id = workorderitem.workorder_id
                LEFT JOIN item ON workorderitem.item_id = item.id
                LEFT JOIN workorderassignee ON workorder.id = workorderassignee.workorder_id
                LEFT JOIN user AS assignee ON workorderassignee.assignee_id = assignee.id
            WHERE
                workorder.department_id IN (
                    SELECT department_id
                    FROM userdepartment
                    WHERE user_id = ?
                )
            GROUP BY
                workorder.id
            ORDER BY
                workorder.id ASC;""",
                (current_user.id,),
            )

        table = main_window.ui.workorder_listingview_tblWorkOrder
        table.clear()
        table.setRowCount(len(rows))
        table.setColumnCount(13)
        table.setHorizontalHeaderLabels(
            [
                "ID",
                "Site",
                "Department",
                "Priority Level",
                "Task Description",
                "Items",
                "Assignees",
                "Comments",
                "Date Allocated",
                "Date Completed",
                "Close Out Comments",
                "Raised By",
                "Date Created",
            ]
        )
        for row_index, row_values in enumerate(rows):
            table.setItem(row_index, 0, QTableWidgetItem(str(row_values[0])))  # ID
            table.setItem(row_index, 1, QTableWidgetItem(row_values[1]))  # Site
            table.setItem(row_index, 2, QTableWidgetItem(row_values[2]))  # Department
            table.setItem(
                row_index, 3, QTableWidgetItem(row_values[3])
            )  # Priority Level
            table.setItem(
                row_index, 4, QTableWidgetItem(row_values[4])
            )  # Task Description
            table.setItem(row_index, 5, QTableWidgetItem(row_values[5]))  # Items
            table.setItem(row_index, 6, QTableWidgetItem(row_values[6]))  # Assignees
            table.setItem(row_index, 7, QTableWidgetItem(row_values[7]))  # Comments
            table.setItem(
                row_index, 8, QTableWidgetItem(row_values[8])
            )  # Date Allocated
            table.setItem(
                row_index, 9, QTableWidgetItem(row_values[9])
            )  # Date Completed
            table.setItem(
                row_index, 10, QTableWidgetItem(row_values[10])
            )  # Close Out Comments
            table.setItem(row_index, 11, QTableWidgetItem(row_values[11]))  # Raised By
            table.setItem(
                row_index, 12, QTableWidgetItem(row_values[12])
            )  # Date Created
