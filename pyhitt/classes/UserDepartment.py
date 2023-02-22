class UserDepartment:
    """
    A class representing a user's department.

    Attributes:
        id (int): The unique identifier of the user department.
        user_id (int): The unique identifier of the user.
        department_id (int): The unique identifier of the department.
    """

    def __init__(self, user_id: int, department_id: int, id_: int = None) -> None:
        """
        Initializes a new instance of the UserDepartment class.

        Parameters:
            user_id (int): The unique identifier of the user.
            department_id (int): The unique identifier of the department.
            id_ (int, optional): The unique identifier of the user department.
        """
        self.id = id
        self.user_id = user_id
        self.department_id = department_id
