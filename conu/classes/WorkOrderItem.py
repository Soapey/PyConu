from dataclasses import dataclass


@dataclass
class WorkOrderItem:
    id: int
    workorder_id: int
    item_id: int
