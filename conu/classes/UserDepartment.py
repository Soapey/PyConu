class UserDepartment:
    def __init__(
        self, id: int = None, user_id: int = None, department_id: int = None
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.department_id = department_id
