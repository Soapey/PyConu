from conu.classes.Base import Base


class PriorityLevel(Base):
    """A class representing a PriorityLevel of a WorkOrder."""

    def __init__(self, name: str, days_until_overdue: int, id_: int = None):
        """Initialize a new PriorityLevel with a name, days until it is overdue, and optional ID."""
        super().__init__(id_)
        self.name = name
        self.days_until_overdue = days_until_overdue

    def __repr__(self) -> str:
        """Return a string representation of the PriorityLevel."""
        values = ', '.join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"{self.__class__.__name__}({values})"
