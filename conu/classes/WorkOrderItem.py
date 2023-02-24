from conu.classes.Base import Base


class WorkOrderItem(Base):
    """A class representing an item in a work order. """

    def __init__(self, workorder_id: int, item_id: int, id_: int = None) -> None:
        """Initializes a new instance of the WorkOrderItem class."""
        super().__init__(id_)
        self.workorder_id = workorder_id
        self.item_id = item_id

    def __repr__(self) -> str:
        """Return a string representation of the WorkOrderItem instance. """
        values = ', '.join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"{self.__class__.__name__}({values})"
