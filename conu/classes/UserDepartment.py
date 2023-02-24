from conu.classes.Base import Base


class UserDepartment(Base):
    """A class representing a user's association with a department."""

    def __init__(self, user_id: int, department_id: int, id_: int = None) -> None:
        """Initialize a new UserDepartment instance."""
        super().__init__(id_)
        self.user_id = user_id
        self.department_id = department_id

    def __repr__(self) -> str:
        """Return a string representation of the UserDepartment instance."""
        values = ', '.join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"{self.__class__.__name__}({values})"

