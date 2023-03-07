CREATE TABLE IF NOT EXISTS [assignee] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] TEXT NOT NULL,
    [description] TEXT
);

CREATE TABLE IF NOT EXISTS [department] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS [assigneedepartment] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [assignee_id] INTEGER NOT NULL,
    [department_id] INTEGER NOT NULL,
    FOREIGN KEY (assignee_id) REFERENCES assignee(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES department(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS [form] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] TEXT NOT NULL,
    [path] TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS [item] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] TEXT NOT NULL,
    [comments] TEXT
);

CREATE TABLE IF NOT EXISTS [itemdepartment] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [item_id] INTEGER NOT NULL,
    [department_id] INTEGER NOT NULL,
    FOREIGN KEY (item_id) REFERENCES item(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES department(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS [prioritylevel] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] TEXT NOT NULL,
    [days_until_overdue] INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS [servicetracker] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [item_id] INTEGER NOT NULL,
    [units_calibration_date] TEXT NOT NULL,
    [current_units] INTEGER NOT NULL,
    [average_units_per_day] INTEGER NOT NULL,
    [service_due_units] INTEGER NOT NULL,
    [service_interval] INTEGER NOT NULL,
    FOREIGN KEY (item_id) REFERENCES item(id) 
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS [site] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] TEXT NOT NULL,
    [address] TEXT,
    [suburb] TEXT
);

CREATE TABLE IF NOT EXISTS [user] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [first_name] TEXT NOT NULL,
    [last_name] TEXT NOT  NULL,
    [job_title] TEXT,
    [email_address] TEXT NOT NULL,
    [username] TEXT NOT NULL,
    [password] TEXT NOT NULL,
    [permission_level] INTEGER NOT NULL,
    [available] INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS [userdepartment] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [user_id] INTEGER NOT NULL,
    [department_id] INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)   
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES department(id) 
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS [workorder] (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [site_id] INTEGER NOT NULL,
    [department_id] INTEGER NOT NULL,
    [prioritylevel_id] NOT NULL,
    [task_description] TEXT NOT NULL,
    [comments] TEXT,
    [date_created] TEXT NOT NULL,
    [date_allocated] TEXT NOT NULL,
    [raisedby_user_id] INTEGER NOT NULL,
    [date_completed] TEXT,
    [purchase_order_number] TEXT,
    [close_out_comments] TEXT,
    FOREIGN KEY (site_id) REFERENCES site(id)
        ON UPDATE CASCADE 
        ON DELETE RESTRICT,
    FOREIGN KEY (department_id) REFERENCES department(id) 
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (prioritylevel_id) REFERENCES prioritylevel(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (raisedby_user_id) REFERENCES user(id) 
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS workorderassignee (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [workorder_id] INTEGER NOT NULL,
    [assignee_id] INTEGER NOT NULL,
    FOREIGN KEY (workorder_id) REFERENCES workorder(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (assignee_id) REFERENCES assignee(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS workorderitem (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [workorder_id] INTEGER NOT NULL,
    [item_id] INTEGER NOT NULL,
    FOREIGN KEY (workorder_id) REFERENCES workorder(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES item(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS recurringworkorder (
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [site_id] INTEGER NOT NULL,
    [department_id] INTEGER NOT NULL,
    [prioritylevel_id] INTEGER NOT NULL,
    [task_description] TEXT NOT NULL,
    [comments] TEXT,
    [type] TEXT NOT NULL,
    [start_date] TEXT NOT NULL,
    [lastraised_date] TEXT NOT NULL,
    [interval] INTEGER,
    [weekdays] TEXT,
    [day] INTEGER,
    [month] INTEGER,
    [month_weekday_occurrence] INTEGER,
    FOREIGN KEY (site_id) REFERENCES site(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (department_id) REFERENCES department(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (prioritylevel_id) REFERENCES prioritylevel(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);