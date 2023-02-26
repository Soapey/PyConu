from conu.classes.Base import Base


class User(Base):
    """Represents a user with their personal and access information."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        job_title: str,
        email_address: str,
        username: str,
        password: str,
        permission_level: int,
        available: bool,
        id_: int = None
    ):
        """Initialize a new user with a first name, last name, job title, email address, username, password, permissiom level and optional ID."""
        super().__init__(id_)
        self.first_name = first_name
        self.last_name = last_name
        self.job_title = job_title
        self.email_address = email_address
        self.username = username
        self.password = password
        self.permission_level = permission_level
        self.available = available

    
    def __repr__(self) -> str:
        """Return a string representation of the user."""
        values = ', '.join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"{self.__class__.__name__}({values})"