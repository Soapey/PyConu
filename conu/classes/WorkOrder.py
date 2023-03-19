from datetime import datetime, date
from conu.classes.PriorityLevel import PriorityLevel
from conu.classes.WorkOrderItem import WorkOrderItem
from conu.classes.WorkOrderAssignee import WorkOrderAssignee
from conu.classes.Item import Item
from conu.classes.Assignee import Assignee
from conu.classes.Site import Site
from conu.classes.Department import Department
from conu.classes.User import User
from conu.db.SQLiteConnection import SQLiteConnection
from conu.db.helpers import select_by_attrs_dict, format_nullable_database_date
from fpdf import FPDF
from conu.helpers import select_file_path, get_max_height
import math


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

        items = select_by_attrs_dict(Item)
        workorderitems = select_by_attrs_dict(WorkOrderItem)

        relevant_workorderitems = {
            workorderitem.id: workorderitem
            for workorderitem in workorderitems.values()
            if workorderitem.workorder_id == self.id
        }

        item_list = list()
        for workorderitem in relevant_workorderitems.values():
            item = items[workorderitem.item_id]
            item_list.append(item.name)

        return ", ".join(item_list)

    def due_listingview_assignees(self):

        assignees = select_by_attrs_dict(Assignee)
        workorderassignees = select_by_attrs_dict(WorkOrderAssignee)

        relevant_workorderassignees = {
            workorderassignee.id: workorderassignee
            for workorderassignee in workorderassignees.values()
            if workorderassignee.workorder_id == self.id
        }

        assignee_list = list()
        for workorderassignee in relevant_workorderassignees.values():
            assignee = assignees[workorderassignee.assignee_id]
            assignee_list.append(assignee.name)

        return ", ".join(assignee_list)

    def due_listingview_summary(self):
        return self.task_description

    def is_due(self) -> bool:

        prioritylevels = select_by_attrs_dict(PriorityLevel)
        priority_level = prioritylevels[self.prioritylevel_id]

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
                format_nullable_database_date(row[6]),
                format_nullable_database_date(row[7]),
                row[8],
                format_nullable_database_date(row[9]),
                row[CELL_HEIGHT_MM],
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

    def site(self):

        sites = select_by_attrs_dict(Site, {"id": self.site_id})

        if sites:
            return sites[self.site_id]

        return None

    def department(self):

        departments = select_by_attrs_dict(Department, {"id": self.department_id})

        if departments:
            return departments[self.department_id]

        return None

    def prioritylevel(self):

        prioritylevels = select_by_attrs_dict(
            PriorityLevel, {"id": self.prioritylevel_id}
        )

        if prioritylevels:
            return prioritylevels[self.prioritylevel_id]

        return None

    def items(self):

        with SQLiteConnection() as cur:

            rows = cur.execute(
                """
            SELECT 
                * 
            FROM 
                item 
            WHERE item.id IN (
                SELECT 
                    workorderitem.item_id 
                FROM 
                    workorderitem 
                WHERE 
                    workorderitem.workorder_id = ?
                );
            """,
                (self.id,),
            ).fetchall()

        return Item.convert_rows_to_instances(rows)

    def assignees(self):

        with SQLiteConnection() as cur:

            rows = cur.execute(
                """
            SELECT 
                * 
            FROM 
                assignee 
            WHERE assignee.id IN (
                SELECT 
                    workorderassignee.assignee_id 
                FROM 
                    workorderassignee
                WHERE 
                    workorderassignee.workorder_id = ?
                );
            """,
                (self.id,),
            ).fetchall()

        return Assignee.convert_rows_to_instances(rows)

    def raisedby(self):

        users = select_by_attrs_dict(User, {"id": self.raisedby_user_id})

        if users:
            return users[self.raisedby_user_id]

        return None

    def save_to_pdf(self):

        A4_WIDTH_MM = 210
        A4_HEIGHT_MM = 297
        A4_MARGIN_MM = 10
        A4_WORKAREA_WIDTH_MM = A4_WIDTH_MM - (A4_MARGIN_MM * 2)
        A4_WORKAREA_HEIGHT_MM = A4_HEIGHT_MM - (A4_MARGIN_MM * 2)
        COLUMNS = 6
        CELL_WIDTH_MM = A4_WORKAREA_WIDTH_MM // COLUMNS
        CELL_HEIGHT_MM = 5

        pdf = FPDF()
        pdf.set_margins(A4_MARGIN_MM, A4_MARGIN_MM, A4_MARGIN_MM)
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        pdf.cell(
            CELL_WIDTH_MM * COLUMNS,
            CELL_HEIGHT_MM,
            f"WORK ORDER",
            align="C",
            border=1,
            ln=1,
        )
        pdf.ln()

        pdf.cell(CELL_WIDTH_MM * 2, CELL_HEIGHT_MM, "Number", align="R", border=1)
        pdf.cell(
            CELL_WIDTH_MM * (COLUMNS - 2),
            CELL_HEIGHT_MM,
            str(self.id),
            border=1,
            ln=1,
        )
        pdf.cell(CELL_WIDTH_MM * 2, CELL_HEIGHT_MM, "Date Created", align="R", border=1)
        pdf.cell(
            CELL_WIDTH_MM * (COLUMNS - 2),
            CELL_HEIGHT_MM,
            datetime.strftime(self.date_created, "%d-%m-%Y"),
            border=1,
            ln=1,
        )

        raisedby = self.raisedby()
        pdf.cell(CELL_WIDTH_MM * 2, CELL_HEIGHT_MM, "Raised By", align="R", border=1)
        pdf.cell(
            CELL_WIDTH_MM * (COLUMNS - 2),
            CELL_HEIGHT_MM,
            f"{raisedby.first_name} {raisedby.last_name}",
            border=1,
            ln=1,
        )
        pdf.cell(
            CELL_WIDTH_MM * 2, CELL_HEIGHT_MM, "Date Allocated", align="R", border=1
        )
        pdf.cell(
            CELL_WIDTH_MM * (COLUMNS - 2),
            CELL_HEIGHT_MM,
            datetime.strftime(self.date_allocated, "%d-%m-%Y"),
            border=1,
            ln=1,
        )
        pdf.cell(CELL_WIDTH_MM * 2, CELL_HEIGHT_MM, "Site", align="R", border=1)
        pdf.cell(
            CELL_WIDTH_MM * (COLUMNS - 2),
            CELL_HEIGHT_MM,
            self.site().name,
            border=1,
            ln=1,
        )
        pdf.cell(CELL_WIDTH_MM * 2, CELL_HEIGHT_MM, "Department", align="R", border=1)
        pdf.cell(
            CELL_WIDTH_MM * (COLUMNS - 2),
            CELL_HEIGHT_MM,
            self.department().name,
            border=1,
            ln=1,
        )
        pdf.cell(
            CELL_WIDTH_MM * 2, CELL_HEIGHT_MM, "Priority Level", align="R", border=1
        )
        pdf.cell(
            CELL_WIDTH_MM * (COLUMNS - 2),
            CELL_HEIGHT_MM,
            self.prioritylevel().name,
            border=1,
            ln=1,
        )
        pdf.cell(
            CELL_WIDTH_MM * 2,
            CELL_HEIGHT_MM,
            "Purchase Order Number",
            align="R",
            border=1,
        )
        pdf.cell(
            CELL_WIDTH_MM * (COLUMNS - 2),
            CELL_HEIGHT_MM,
            self.purchase_order_number,
            border=1,
            ln=1,
        )
        pdf.ln()

        pdf.cell(
            CELL_WIDTH_MM * COLUMNS,
            CELL_HEIGHT_MM,
            "TASK DESCRIPTION",
            border=1,
            align="C",
            ln=1,
        )
        pdf.multi_cell(
            CELL_WIDTH_MM * COLUMNS,
            get_max_height(self.task_description, pdf, CELL_WIDTH_MM * COLUMNS),
            self.task_description,
            border=1,
        )
        pdf.ln()
        pdf.ln()

        sections = 3

        pdf.cell(CELL_WIDTH_MM * COLUMNS, CELL_HEIGHT_MM, "ITEMS", border=1, align="C")
        pdf.ln()
        for index, item in enumerate(self.items().values()):
            pdf.cell(CELL_WIDTH_MM * 2, CELL_HEIGHT_MM, item.name, border=1)
            if (index + 1) % sections == 0:
                pdf.ln()
        pdf.ln()
        pdf.ln()

        pdf.cell(
            CELL_WIDTH_MM * COLUMNS, CELL_HEIGHT_MM, "ASSIGNEES", border=1, align="C"
        )
        pdf.ln()
        for index, assignee in enumerate(self.assignees().values()):
            pdf.cell(CELL_WIDTH_MM * 2, CELL_HEIGHT_MM, assignee.name, border=1)
            if (index + 1) % sections == 0:
                pdf.ln()
        pdf.ln()
        pdf.ln()

        pdf.cell(
            CELL_WIDTH_MM * COLUMNS,
            CELL_HEIGHT_MM,
            "COMMENTS",
            border=1,
            align="C",
            ln=1,
        )
        pdf.multi_cell(
            CELL_WIDTH_MM * COLUMNS,
            get_max_height(self.comments, pdf, CELL_WIDTH_MM * COLUMNS),
            self.comments,
            border=1,
        )
        pdf.ln()
        pdf.ln()

        pdf.cell(
            CELL_WIDTH_MM * COLUMNS,
            CELL_HEIGHT_MM,
            "CLOSE OUT COMMENTS",
            border=1,
            align="C",
            ln=1,
        )
        if self.date_completed and self.close_out_comments:
            pdf.multi_cell(
                CELL_WIDTH_MM * COLUMNS,
                get_max_height(self.close_out_comments, pdf, CELL_WIDTH_MM * COLUMNS),
                self.close_out_comments,
                border=1,
            )
        else:
            pdf.cell(CELL_WIDTH_MM * COLUMNS, CELL_HEIGHT_MM, border=1)
        pdf.ln()

        pdf.cell(
            CELL_WIDTH_MM * 2,
            CELL_HEIGHT_MM,
            "Date Completed",
            align="R",
            border=1,
        )

        if self.date_completed:
            pdf.cell(
                CELL_WIDTH_MM * (COLUMNS - 2),
                CELL_HEIGHT_MM,
                datetime.strftime(self.date_completed, "%d-%m-%Y"),
                border=1,
                ln=1,
            )
        else:
            pdf.cell(
                CELL_WIDTH_MM * (COLUMNS - 2),
                CELL_HEIGHT_MM,
                border=1,
                ln=1,
            )

        pdf.ln()
        pdf.ln()

        file_path = select_file_path()

        if file_path:
            pdf.output(file_path, "F")
            print("Work order document created and saved successfully!")
        else:
            print("No file path selected, work order document not created.")


if __name__ == "__main__":

    wo = list(WorkOrder.get().values())[0]
    wo.save_to_pdf()
