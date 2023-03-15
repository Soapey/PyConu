from datetime import datetime, date
from conu.classes.PriorityLevel import PriorityLevel
from conu.db.SQLiteConnection import SQLiteConnection
from conu.db.helpers import select_by_attrs_dict, format_nullable_database_date


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
    def get_listingview_table_data(cls, main_window):

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
                workorder.comments,
                GROUP_CONCAT(DISTINCT item.name),
                GROUP_CONCAT(DISTINCT assignee.name),
                strftime('%d-%m-%Y', workorder.date_allocated),
                strftime('%d-%m-%Y', workorder.date_completed),
                workorder.close_out_comments,
                user.first_name || ' ' || user.last_name,
                strftime('%d-%m-%Y', workorder.date_created)
            FROM
                workorder
                JOIN site ON workorder.site_id = site.id
                JOIN department ON workorder.department_id = department.id
                JOIN prioritylevel ON workorder.prioritylevel_id = prioritylevel.id
                JOIN user ON workorder.raisedby_user_id = user.id
                LEFT JOIN workorderitem ON workorder.id = workorderitem.workorder_id
                LEFT JOIN item ON workorderitem.item_id = item.id
                LEFT JOIN workorderassignee ON workorder.id = workorderassignee.workorder_id
                LEFT JOIN assignee ON workorderassignee.assignee_id = assignee.id
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
            ).fetchall()

        return rows

    @classmethod
    def get(cls):

        with SQLiteConnection() as cur:

            rows = cur.execute("SELECT * FROM workorder;").fetchall()

        return {
            row[0]: cls(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                format_nullable_database_date(row[6]),
                format_nullable_database_date(row[7]),
                row[8],
                format_nullable_database_date(row[9]),
                row[10],
                row[11],
            )
            for row in rows
        }
