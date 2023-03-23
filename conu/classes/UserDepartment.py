from dataclasses import dataclass


@dataclass
class UserDepartment:
    id: int
    user_id: int
    department_id: int
