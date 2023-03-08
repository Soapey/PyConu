from datetime import date
from dataclasses import dataclass
from conu.db.SQLiteConnection import select_by_attrs_dict
from conu.classes.PriorityLevel import PriorityLevel


@dataclass
class WorkOrder:
    # WorkOrderBase properties
    id: int
    site_id: int
    department_id: int
    prioritylevel_id: int
    task_description: str
    comments: str

    # WorkOrder specific properties
    date_created: date
    date_allocated: date
    raisedby_user_id: int
    date_completed: date
    purchase_order_number: str
    close_out_comments: str

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
