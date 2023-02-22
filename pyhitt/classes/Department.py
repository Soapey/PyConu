class Department:
    """
    A class representing a department in a company.

    Attributes:
        id_ (int): The unique identifier of the department.
        name (str): The name of the department.
        available (bool): Whether the department is available.
    """

    def __init__(self, name: str, available: bool, id_: int = None) -> None:
        """
        Initializes a new instance of the Department class.

        Args:
            id_ (int, optional): The unique identifier of the department. Defaults to None.
            name (str, optional): The name of the department.
            available (bool, optional): Whether the department is available.
        """
        self.id_ = id_
        self.name = name
        self.available = available
