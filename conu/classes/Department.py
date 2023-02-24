from conu.classes.Base import Base


class Department(Base):
    """A class representing a department."""

    def __init__(self, name: str, available: bool, id_: int = None) -> None:
        """Initialize a new department with a name and availability status."""
        super().__init__(id_)
        self.name = name
        self.available = available

    def __repr__(self) -> str:
        """Return a string representation of the department."""
        values = ', '.join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"{self.__class__.__name__}({values})"