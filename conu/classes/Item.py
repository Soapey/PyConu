from conu.classes.Base import Base


class Item(Base):
    """A class representing an item."""

    def __init__(self, name: str, comments: str, id_: int = None):
        """Initialize a new item with a name, comments, and optional ID."""
        super().__init__(id_)
        self.name = name
        self.comments = comments
        
    def __repr__(self) -> str:
        """Return a string representation of the item."""
        values = ', '.join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"{self.__class__.__name__}({values})"
