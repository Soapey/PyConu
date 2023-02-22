class Item:
    """
    Represents an item with various attributes.

    Attributes:
        id (int): The unique identifier for the item.
        name (str): The name of the item.
        comments (str): Comments or additional information about the item.
    """

    def __init__(self, name: str, comments: str, id_: int = None):
        """
        Initializes a new instance of the Item class with the specified attributes.

        Parameters:
            name (str): The name of the item.
            comments (str): Comments or additional information about the item.
            id_ (int, optional): The unique identifier for the item.
        """
        self.id = id_
        self.name = name
        self.comments = comments
