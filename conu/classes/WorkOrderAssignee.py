from conu.classes.Base import Base


class WorkOrderAssignee(Base):
    """A class representing the assignee of the WorkOrder."""

    def __init__(self, workorder_id: int, assignee_id: int, id_: int = None) -> None:
        """Initializes a new instance of the WorkOrderAssignee class."""
        super().__init__(id_)
        self.workorder_id = workorder_id
        self.assignee_id = assignee_id

    def __repr__(self) -> str:
        """Return a string representation of the WorkOrderAssignee instance. """
        values = ', '.join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"{self.__class__.__name__}({values})"
