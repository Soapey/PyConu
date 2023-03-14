from dataclasses import dataclass


@dataclass
class WorkOrderAssignee:
    id: int
    workorder_id: int
    assignee_id: int

    def __eq__(self, __o: object) -> bool:
        return self.id == __o.id
