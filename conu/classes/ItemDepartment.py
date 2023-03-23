from dataclasses import dataclass


@dataclass
class ItemDepartment:
    id: int
    item_id: int
    department_id: int