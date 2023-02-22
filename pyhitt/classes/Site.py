class Site:
    """
    A class representing a site.

    Attributes:
        id (int): The unique identifier of the site.
        name (str): The name of the site.
        address (str): The address of the site.
        suburb (str): The suburb where the site is located.
        available (bool): Whether the site is available.
    """

    def __init__(self, name: str, address: str, suburb: str, available: bool, id_: int = None) -> None:
        """
        Initializes a new instance of the Site class.

        Args:
            id (int, optional): The unique identifier of the site.
            name (str): The name of the site.
            address (str): The address of the site.
            suburb (str): The suburb where the site is located.
            available (bool): Whether the site is available.
        """
        self.id = id_
        self.name = name
        self.address = address
        self.suburb = suburb
        self.available = available
