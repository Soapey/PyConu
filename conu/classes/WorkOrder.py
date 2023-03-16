from datetime import datetime, date
from conu.classes.PriorityLevel import PriorityLevel
from conu.classes.WorkOrderItem import WorkOrderItem
from conu.classes.Item import Item
from conu.classes.Assignee import Assignee
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

    def due_listingview_items(self):

        global global_items
        global global_workorderitems

        relevant_workorderitems = {
            workorderitem.id: workorderitem
            for workorderitem in global_workorderitems.values()
            if workorderitem.workorder_id == self.id
        }

        item_list = list()
        for workorderitem in relevant_workorderitems.values():
            if workorderitem.item_id not in global_items.keys():
                global_items = select_by_attrs_dict(Item)
            item = global_items[workorderitem.item_id]
            item_list.append(item.name)

        return ", ".join(item_list)

    def due_listingview_assignees(self):

        global global_assignees
        global global_workorderassignees

        relevant_workorderassignees = {
            workorderassignee.id: workorderassignee
            for workorderassignee in global_workorderassignees.values()
            if workorderassignee.workorder_id == self.id
        }

        assignee_list = list()
        for workorderassignee in relevant_workorderassignees.values():
            if workorderassignee.assignee_id not in global_assignees.keys():
                global_assignees = select_by_attrs_dict(Assignee)
            assignee = global_assignees[workorderassignee.assignee_id]
            assignee_list.append(assignee.name)

        return ", ".join(assignee_list)

    def summary(self):
        return self.task_description

    def is_due(self) -> bool:

        global global_prioritylevels

        if self.prioritylevel_id not in global_prioritylevels.keys():
            global_prioritylevels = select_by_attrs_dict(PriorityLevel)
        priority_level = global_prioritylevels[self.prioritylevel_id]

        days_until_overdue = priority_level.days_until_overdue

        return (
            not self.date_completed
            and (date.today() - self.date_allocated).days >= days_until_overdue
        )

    @classmethod
    def convert_rows_to_instances(cls, rows):

        return {
            row[0]: cls(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                format_nullable_database_date(row[6]).date(),
                format_nullable_database_date(row[7]).date(),
                row[8],
                format_nullable_database_date(row[9]).date(),
                row[10],
                row[11],
            )
            for row in rows
        }

    @classmethod
    def get_by_user_departments(cls, user_id):

        with SQLiteConnection() as cur:

            rows = cur.execute(
                """
                SELECT 
                    * 
                FROM 
                    workorder 
                WHERE 
                    workorder.department_id IN 
                        (SELECT userdepartment.department_id FROM userdepartment WHERE userdepartment.user_id = ?);""",
                (user_id,),
            ).fetchall()

        return cls.convert_rows_to_instances(rows)

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
