from datetime import date
from dataclasses import dataclass


@dataclass
class WorkOrder:
    id: int
    site_id: int
    department_id: int
    prioritylevel_id: int
    date_created: date
    date_allocated: date
    task_description: str
    raisedby_user_id: int
    date_completed: date
    purchase_order_number: str
    comments: str
    close_out_comments: str
