class AssigneeDepartment:
    def __init__(
        self, id: int = None, assignee_id: int = None, department_id: int = None
    ) -> None:
        self.id = id
        self.assignee_id = assignee_id
        self.department_id = department_id
