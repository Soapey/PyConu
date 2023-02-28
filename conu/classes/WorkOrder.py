from datetime import date
from dataclasses import dataclass


@dataclass
class WorkOrder:
    id: int
    site_id: int
    department_id: int
    prioritylevel_id: int
    task_description: str
    comments: str

    date_created: date
    date_allocated: date
    raisedby_user_id: int
    date_completed: date
    purchase_order_number: str
    close_out_comments: str
