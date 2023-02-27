from dataclasses import dataclass


@dataclass
class AssigneeDepartment:
    id: int
    assignee_id: int
    department_id: int