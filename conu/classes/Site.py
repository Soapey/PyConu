from conu.classes.Base import Base


class Site(Base):
    """A class representing a site."""

    def __init__(self, name: str, address: str, suburb: str, available: bool, id_: int = None) -> None:
        """Initialize a new site with a name, address, suburb, availability, and optional ID."""
        super().__init__(id_)
        self.name = name
        self.address = address
        self.suburb = suburb
        self.available = available

    def __repr__(self) -> str:
        """Return a string representation of the site."""
        values = ', '.join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"{self.__class__.__name__}({values})"
