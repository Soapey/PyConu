from pyhitt.classes.Base import Base


class Assignee(Base):
    """A class representing an assignee for a task."""

    def __init__(self, name: str, description: str, id_: int = None):
        """Initialize a new assignee with a name, description, and optional ID."""
        super().__init__(id_)
        self.name = name
        self.description = description

    def __repr__(self) -> str:
        """Return a string representation of the assignee."""
        values = ', '.join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"{self.__class__.__name__}({values})"