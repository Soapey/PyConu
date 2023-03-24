class WorkOrderAssignee:
    def __init__(
        self, id: int = None, workorder_id: int = None, assignee_id: int = None
    ) -> None:
        self.id = id
        self.workorder_id = workorder_id
        self.assignee_id = assignee_id

    def __eq__(self, __o: object) -> bool:
        return (
            self.id == __o.id
            and self.workorder_id == __o.workorder_id
            and self.assignee_id == __o.assignee_id
        )
