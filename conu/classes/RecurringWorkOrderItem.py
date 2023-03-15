from dataclasses import dataclass


@dataclass
class RecurringWorkOrderItem:
    id: int
    recurringworkorder_id: int
    item_id: int

    def __eq__(self, __o: object) -> bool:
        return self.id == __o.id
