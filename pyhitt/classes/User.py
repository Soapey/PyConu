class User:
    """
    Represents a user with various attributes such as ID, name, job title, email, username, password, and permission level.

    Attributes:
        id (int, optional): The unique identifier for the user.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        job_title (str): The user's job title.
        email_address (str): The user's email address.
        username (str): The user's username.
        password (str): The user's password.
        permission_level (int): The user's permission level.
        available (bool): Whether the user is available.
    """

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
        """
        Initializes a new instance of the User class with the specified attributes.

        Parameters:
            first_name (str): The user's first name.
            last_name (str): The user's last name.
            job_title (str): The user's job title.
            email_address (str): The user's email address.
            username (str): The user's username.
            password (str): The user's password.
            permission_level (int): The user's permission level.
            available (bool): Whether the user is available.
            id_ (int, optional): The unique identifier for the user.
        """
        self.id = id_
        self.first_name = first_name
        self.last_name = last_name
        self.job_title = job_title
        self.email_address = email_address
        self.username = username
        self.password = password
        self.permission_level = permission_level
        self.available = available
