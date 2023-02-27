from dataclasses import dataclass


@dataclass
class WorkOrderAssignee:
    id: int
    workorder_id: int
    assignee_id: int
