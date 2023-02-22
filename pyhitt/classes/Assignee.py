class Assignee:
    """
    Represents an assignee with various attributes such as ID, name, and description.

    Attributes:
        id (int): The unique identifier for the assignee.
        name (str): The name of the assignee.
        description (str): The description of the assignee.
    """

    def __init__(self, name: str, description: str, id_: int = None):
        """
        Initializes a new instance of the Assignee class with the specified attributes.

        Parameters:
            name (str): The name of the assignee.
            description (str): The description of the assignee.
            id_ (int, optional): The unique identifier for the assignee.
        """
        self.id = id_
        self.name = name
        self.description = description
