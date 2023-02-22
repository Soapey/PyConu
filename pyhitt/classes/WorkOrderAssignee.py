class WorkOrderAssignee:
    """
    A class representing an assignee for a work order.

    Attributes:
        id (int): The ID of the work order assignee (optional).
        workorder_id (int): The ID of the work order associated with the assignee.
        assignee_id (int): The ID of the assignee associated with the work order.
    """

    def __init__(self, workorder_id: int, assignee_id: int, id_: int = None) -> None:
        """
        Initializes a new instance of the WorkOrderAssignee class.

        Parameters:
            workorder_id (int): The ID of the work order associated with the assignee.
            assignee_id (int): The ID of the assignee associated with the work order.
            id (int, optional): The ID of the work order assignee. Defaults to None.
        """
        self.id = id_
        self.workorder_id = workorder_id
        self.assignee_id = assignee_id
