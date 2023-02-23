from datetime import date
from pyhitt.classes.Base import Base


class WorkOrder(Base):
    """A class representing a work order for a task at a site."""

    def __init__(
        self,
        site_id: int,
        department_id: int,
        prioritylevel_id: int,
        date_created: date,
        date_allocated: date,
        task_description: str,
        raisedby_user_id: int,
        date_completed: date = None,
        purchase_order_number: str = None,
        comments: str = None,
        close_out_comments: str = None,
        id_: int = None,
    ) -> None:
        """Initialize a new WorkOrder instance. """
        super().__init__(id_)
        self.site_id = site_id
        self.department_id = department_id
        self.prioritylevel_id = prioritylevel_id
        self.date_created = date_created
        self.date_allocated = date_allocated
        self.date_completed = date_completed
        self.task_description = task_description
        self.purchase_order_number = purchase_order_number
        self.raisedby_user_id = raisedby_user_id
        self.comments = comments
        self.close_out_comments = close_out_comments

    def __repr__(self) -> str:
        """Return a string representation of the WorkOrder instance. """
        values = ', '.join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"{self.__class__.__name__}({values})"

