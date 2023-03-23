from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import calendar
from conu.db.SQLiteConnection import SQLiteConnection
from conu.db.helpers import format_nullable_database_date, select_by_attrs_dict
from conu.classes.Item import Item
from conu.classes.Site import Site
from conu.classes.Department import Department
from conu.classes.PriorityLevel import PriorityLevel
from conu.classes.RecurringWorkOrderItem import RecurringWorkOrderItem


class RecurringWorkOrder:
    def __init__(
        self,
        id: int = None,
        site_id: int = None,
        department_id: int = None,
        prioritylevel_id: int = None,
        task_description: str = None,
        comments: str = None,
        type: str = None,
        start_date: date = None,
        lastraised_date: date = None,
        interval: int = None,
        weekdays: str = None,
        day: int = None,
        month: int = None,
        month_weekday_occurrence: int = None,
    ):
        self.id = id
        self.site_id = site_id
        self.department_id = department_id
        self.prioritylevel_id = prioritylevel_id
        self.task_description = task_description
        self.comments = comments
        self.type = type
        self.start_date = start_date
        self.lastraised_date = lastraised_date
        self.interval = interval
        self.weekdays = weekdays
        self.day = day
        self.month = month
        self.month_weekday_occurrence = month_weekday_occurrence

    def __str__(self) -> str:
        type = self.type.strip().lower()
        weekdays = (
            [int(wd) for wd in self.weekdays.split(";")] if self.weekdays else list()
        )

        if type == "daily":
            if self.interval:
                return f"Occur every {self.interval} days"
            else:
                return f"Occur on every {', '.join(calendar.day_name[wd-1] for wd in weekdays)}"
        elif type == "weekly":
            return f"Occur every {self.interval} week(s) on {', '.join(calendar.day_name[wd-1] for wd in weekdays)}"
        elif type == "monthly":
            if self.day and self.interval:
                return f"Occur on day {self.day} of every {self.interval} month(s)"
            else:
                month_weekday_occurrence = (
                    "last"
                    if self.month_weekday_occurrence > 3
                    else self.month_weekday_occurrence
                )
                return f"Occur on the {month_weekday_occurrence} occurrence of {calendar.day_name[weekdays[0]-1]}, every {self.interval} month(s)"
        elif type == "yearly":
            if self.month and self.day:
                return f"Occur every {self.interval} year(s) on {calendar.month_name[self.month - 1]} {self.day}"
            else:
                month_weekday_occurrence = (
                    "last"
                    if self.month_weekday_occurrence > 3
                    else self.month_weekday_occurrence
                )
                return f"Occur every {self.interval} year(s) on the {month_weekday_occurrence} occurrence of {calendar.day_name[weekdays[0]-1]} in {calendar.month_name[self.month-1]}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"

    def due_listingview_items(self):

        items = select_by_attrs_dict(Item)
        recurringworkorderitems = select_by_attrs_dict(RecurringWorkOrderItem)

        relevant_recurringworkorderitems = {
            recurringworkorderitem.id: recurringworkorderitem
            for recurringworkorderitem in recurringworkorderitems.values()
            if recurringworkorderitem.recurringworkorder_id == self.id
        }

        item_list = list()
        for recurringworkorderitem in relevant_recurringworkorderitems.values():
            item = items[recurringworkorderitem.item_id]
            item_list.append(item.name)

        return ", ".join(item_list)

    def due_listingview_assignees(self):
        return str()

    def due_listingview_summary(self):
        return self.task_description

    def is_due(self):

        occurrences = list()
        d = self.start_date
        todays_date = date.today()
        type = self.type.strip().lower()

        if self.weekdays:
            weekdays = [int(wd) for wd in self.weekdays.split(";")]

        while d <= todays_date:

            date_step = timedelta(days=1)

            if type == "daily":

                if self.interval:
                    occurrences.append(d)
                    date_step = timedelta(days=self.interval)

                elif self.weekdays:
                    if d.isoweekday() in weekdays:
                        occurrences.append(d)

            elif type == "weekly":

                monday_date = d - timedelta(days=d.isoweekday() - 1)

                for i in range(7):
                    week_date = monday_date + timedelta(days=i)
                    if (
                        week_date.isoweekday() in weekdays
                        and week_date <= date.today()
                        and week_date > self.lastraised_date
                    ):
                        occurrences.append(week_date)

                date_step = timedelta(days=7 * self.interval)

            elif type == "monthly":

                relative = relativedelta(d, self.start_date)

                # By day number of month interval
                if self.day and self.interval:

                    if (
                        d.day == self.day
                        and (relative.months + relative.years * 12) % self.interval == 0
                    ):
                        occurrences.append(d)

                    date_step = timedelta(days=1)

                # By weekday occurrence of month interval
                elif self.month_weekday_occurrence and self.weekdays and self.interval:

                    if relative.months % self.interval == 0:
                        dates = list()

                        _d = date(d.year, d.month, 1)
                        while _d.month == d.month and _d.year == d.year:

                            if _d.isoweekday() == weekdays[0]:
                                dates.append(_d)

                            _d += timedelta(days=1)

                        index = (
                            self.month_weekday_occurrence
                            if self.month_weekday_occurrence <= 3
                            else -1
                        )
                        occurrences.append(dates[index])

                        next_month_mod = (d.month + 1) % 12
                        years_to_add = d.month // 12
                        next_month_date = date(
                            d.year + years_to_add,
                            12 if next_month_mod == 0 else next_month_mod,
                            1,
                        )
                        days_to_add = next_month_date - d
                        date_step = timedelta(days=days_to_add.days)

            elif type == "yearly":

                if self.interval:
                    years_difference = self.start_date.year - d.year
                    if years_difference % self.interval == 0 and d.month == self.month:

                        # By day, month number
                        if self.month and self.day:

                            occurrences.append(date(d.year, self.month, self.day))
                            date_step = timedelta(days=365)

                        # By weekday occurence of month number and year interval
                        elif (
                            self.month_weekday_occurrence
                            and self.weekdays
                            and self.month
                        ):

                            dates = list()

                            _d = date(d.year, d.month, 1)
                            while _d.month == d.month and _d.year == d.year:

                                if _d.isoweekday() == weekdays[0]:
                                    dates.append(_d)

                                _d += timedelta(days=1)

                            index = (
                                self.month_weekday_occurrence - 1
                                if self.month_weekday_occurrence <= 3
                                else -1
                            )
                            occurrences.append(dates[index])

                            next_month_mod = (d.month + 1) % 12
                            years_to_add = d.month // 12
                            next_month_date = date(
                                d.year + years_to_add,
                                12 if next_month_mod == 0 else next_month_mod,
                                1,
                            )
                            days_to_add = next_month_date - d
                            date_step = timedelta(days=days_to_add.days)

            d += date_step

        occurrences = sorted(
            list(
                filter(
                    lambda o: o > self.lastraised_date and o <= todays_date, occurrences
                )
            )
        )
        if occurrences:
            print(occurrences)
            return todays_date >= occurrences[-1]
        return False

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
                row[6],
                format_nullable_database_date(row[7]),
                format_nullable_database_date(row[8]),
                row[9],
                row[10],
                row[11],
                row[12],
                row[13],
            )
            for row in rows
        }

    @classmethod
    def get(cls):

        with SQLiteConnection() as cur:

            rows = cur.execute("SELECT * FROM recurringworkorder;").fetchall()

        return cls.convert_rows_to_instances(rows)

    @classmethod
    def get_by_user_departments(cls, user_id):

        with SQLiteConnection() as cur:

            rows = cur.execute(
                """
                SELECT * 
                FROM recurringworkorder 
                JOIN userdepartment ON recurringworkorder.department_id = userdepartment.department_id
                WHERE userdepartment.user_id = ?;""",
                (user_id,),
            ).fetchall()

        return cls.convert_rows_to_instances(rows)

    @classmethod
    def get_listingview_table_data(cls, main_window):

        current_user = main_window.current_user

        if not current_user:
            return

        recurringworkorders = cls.get_by_user_departments(current_user.id)

        sites = select_by_attrs_dict(Site)
        departments = select_by_attrs_dict(Department)
        prioritylevels = select_by_attrs_dict(PriorityLevel)

        data = [
            (
                rwo.id,
                sites[rwo.site_id].name,
                departments[rwo.department_id].name,
                prioritylevels[rwo.prioritylevel_id].name,
                rwo.task_description,
                rwo.comments,
                rwo.__str__(),
                rwo.is_due(),
            )
            for rwo in recurringworkorders.values()
        ]

        return data
