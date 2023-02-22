from datetime import date


class WorkOrder:
    """
    A class representing a work order.

    Attributes:
        id (int): The ID of the work order (optional).
        site_id (int): The ID of the site where the work order needs to be performed.
        department_id (int): The ID of the department associated with the work order.
        prioritylevel_id (int): The ID of the priority level associated with the work order.
        date_created (date): The date on which the work order was created.
        date_allocated (date): The date on which the work order was allocated.
        date_completed (date): The date on which the work order was completed (optional).
        task_description (str): A description of the task associated with the work order.
        purchase_order_number (str): The purchase order number associated with the work order (optional).
        raisedby_user_id (int): The ID of the user who raised the work order.
        comments (str): Any additional comments associated with the work order (optional).
        close_out_comments (str): Comments regarding the work order's close out status (optional).
    """

    def __init__(
        self,
        site_id: int,
        department_id: int,
        prioritylevel_id: int,
        date_created: date,
        date_allocated: date,
        task_description: str,
        raisedby_user_id: int,
        date_completed: date = None,
        purchase_order_number: str = None,
        comments: str = None,
        close_out_comments: str = None,
        id_: int = None,
    ) -> None:
        """
        Initializes a new instance of the WorkOrder class.

        Parameters:
            site_id (int): The ID of the site where the work order needs to be performed.
            department_id (int): The ID of the department associated with the work order.
            prioritylevel_id (int): The ID of the priority level associated with the work order.
            date_created (date): The date on which the work order was created.
            date_allocated (date): The date on which the work order was allocated.
            task_description (str): A description of the task associated with the work order.
            raisedby_user_id (int): The ID of the user who raised the work order.
            date_completed (date, optional): The date on which the work order was completed. Defaults to None.
            purchase_order_number (str, optional): The purchase order number associated with the work order. Defaults to None.
            comments (str, optional): Any additional comments associated with the work order. Defaults to None.
            close_out_comments (str, optional): Comments regarding the work order's close out status. Defaults to None.
            id_ (int, optional): The ID of the work order. Defaults to None.
        """
        self.id = id_
        self.site_id = site_id
        self.department_id = department_id
        self.prioritylevel_id = prioritylevel_id
        self.date_created = date_created
        self.date_allocated = date_allocated
        self.date_completed = date_completed
        self.task_description = task_description
        self.purchase_order_number = purchase_order_number
        self.raisedby_user_id = raisedby_user_id
        self.comments = comments
        self.close_out_comments = close_out_comments
