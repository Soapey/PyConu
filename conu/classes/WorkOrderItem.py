class WorkOrderItem:
    def __init__(
        self, id: int = None, workorder_id: int = None, item_id: int = None
    ) -> None:
        self.id = id
        self.workorder_id = workorder_id
        self.item_id = item_id

    def __eq__(self, __o: object) -> bool:
        return self.id == __o.id
