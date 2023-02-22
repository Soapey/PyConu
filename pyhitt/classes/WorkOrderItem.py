class WorkOrderItem:
    """
    A class representing an item in a work order.

    Attributes:
        id (int): The ID of the work order item (optional).
        workorder_id (int): The ID of the work order associated with the item.
        item_id (int): The ID of the item associated with the work order.
    """

    def __init__(self, workorder_id: int, item_id: int, id_: int = None) -> None:
        """
        Initializes a new instance of the WorkOrderItem class.

        Parameters:
            workorder_id (int): The ID of the work order associated with the item.
            item_id (int): The ID of the item associated with the work order.
            id_ (int, optional): The ID of the work order item. Defaults to None.
        """
        self.id = id
        self.workorder_id = workorder_id
        self.item_id = item_id
