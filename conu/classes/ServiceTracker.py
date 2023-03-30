from datetime import datetime, date
from conu.db.QueryExporter import QueryExporter
from conu.db.SQLiteConnection import SQLiteConnection
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem
from conu.db.helpers import select_by_attrs_dict, format_nullable_database_date
from conu.helpers import select_directory
from conu.classes.Item import Item


class ServiceTracker:
    def __init__(
        self,
        id: int = None,
        item_id: int = None,
        units_calibration_date: date = None,
        current_units: int = None,
        average_units_per_day: int = None,
        service_due_units: int = None,
        service_interval: int = None,
    ) -> None:
        self.id = id
        self.item_id = item_id
        self.units_calibration_date = units_calibration_date
        self.current_units = current_units
        self.average_units_per_day = average_units_per_day
        self.service_due_units = service_due_units
        self.service_interval = service_interval

    def __str__(self) -> str:
        items = select_by_attrs_dict(Item)
        item = items[self.item_id]
        return f"{item.name} {self.service_due_units} unit service. Due every {self.service_interval} units."

    def is_due(self) -> bool:

        days_since_calibration = (date.today() - self.units_calibration_date).days
        estimated_current_units = self.current_units + (
            days_since_calibration * self.average_units_per_day
        )
        return estimated_current_units >= self.service_due_units

    def due_listingview_items(self):

        items = select_by_attrs_dict(Item)

        item = items[self.item_id]

        return item.name

    def due_listingview_assignees(self):
        return str()

    def due_listingview_summary(self):
        return f"{self.service_due_units} unit service."

    @classmethod
    def select_by_attr_dict(cls, attrs: dict = None) -> dict:

        with SQLiteConnection() as cur:

            if not attrs:
                query = f"SELECT * FROM {cls.__name__.lower()}"
                results = cur.execute(query).fetchall()
            else:
                # Build the SQL query dynamically
                query = f"SELECT * FROM {cls.__name__.lower()} WHERE "
                query += " AND ".join(f"{key} = ?" for key in attrs.keys())

                # Execute the query and fetch the results
                data = cur.execute(query, list(attrs.values()))
                results = data.fetchall()

            # Map the results to objects and return as a dictionary
            objects = dict()
            for row in results:
                (
                    id,
                    item_id,
                    units_calibration_date,
                    current_units,
                    average_units_per_day,
                    service_due_units,
                    service_interval,
                ) = row

                entity: ServiceTracker = cls(
                    id=id,
                    item_id=item_id,
                    units_calibration_date=datetime.strptime(
                        units_calibration_date, "%Y-%m-%d"
                    ).date(),
                    current_units=current_units,
                    average_units_per_day=average_units_per_day,
                    service_due_units=service_due_units,
                    service_interval=service_interval,
                )

                objects[entity.id] = entity

            return objects

    @classmethod
    def load_entities_into_table(cls, table, entities: list = None):

        if not entities:
            entities = list(cls.select_by_attr_dict().values())

        items = select_by_attrs_dict(Item)

        # Create a QTableWidget with the correct number of rows and columns
        headers = [
            "ID",
            "Item",
            "Calibration Date",
            "Current Units",
            "Average Units per Day",
            "Service Due Units",
            "Service Interval Units",
            "Is Due",
        ]

        table.clear()
        table.setRowCount(len(entities))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        horizontal_header = table.horizontalHeader()

        # Loop through each entity and attribute

        for header_index, _ in enumerate(headers):

            horizontal_header.setSectionResizeMode(
                header_index, QHeaderView.ResizeToContents
            )

        for row_index, entity in enumerate(entities):

            item = items[entity.item_id]

            table.setItem(row_index, 0, QTableWidgetItem(str(entity.id)))
            table.setItem(row_index, 1, QTableWidgetItem(item.name))
            table.setItem(
                row_index,
                2,
                QTableWidgetItem(
                    datetime.strftime(entity.units_calibration_date, "%d-%m-%Y")
                ),
            )
            table.setItem(row_index, 3, QTableWidgetItem(str(entity.current_units)))
            table.setItem(
                row_index, 4, QTableWidgetItem(str(entity.average_units_per_day))
            )
            table.setItem(row_index, 5, QTableWidgetItem(str(entity.service_due_units)))
            table.setItem(row_index, 6, QTableWidgetItem(str(entity.service_interval)))
            table.setItem(row_index, 7, QTableWidgetItem(str(entity.is_due())))

    @classmethod
    def convert_rows_to_instances(cls, rows):

        return {
            row[0]: cls(
                row[0],
                row[1],
                format_nullable_database_date(row[2]),
                row[3],
                row[4],
                row[5],
                row[6],
            )
            for row in rows
        }

    @classmethod
    def get(cls):

        with SQLiteConnection() as cur:

            rows = cur.execute(
                """
                SELECT * 
                FROM servicetracker;
                """
            ).fetchall()

        return cls.convert_rows_to_instances(rows)

    @classmethod
    def get_by_user_departments(cls, user_id):

        with SQLiteConnection() as cur:

            rows = cur.execute(
                """
                SELECT DISTINCT st.*
                FROM servicetracker st
                JOIN itemdepartment id ON st.item_id = id.item_id
                JOIN userdepartment ud ON id.department_id = ud.department_id
                WHERE ud.user_id = ?
                """,
                (user_id,),
            ).fetchall()

        return cls.convert_rows_to_instances(rows)
    
    @classmethod
    def get_listingview_table_data(cls, main_window, export_to_excel = False):

        current_user = main_window.current_user

        if not current_user:
            return

        query = """
                SELECT DISTINCT
                    st.id AS 'ID',
                    i.name AS 'Item',
                    st.units_calibration_date AS 'Units Calibration Date',
                    st.current_units AS 'Current Units',
                    st.average_units_per_day AS 'Average Units per Day',
                    st.service_due_units AS 'Service Due Units',
                    st.service_interval AS 'Service Interval Units'
                FROM servicetracker st
                JOIN item i ON st.item_id = i.id
                JOIN itemdepartment id ON st.item_id = id.item_id
                JOIN userdepartment ud ON id.department_id = ud.department_id
                WHERE ud.user_id = ?
                """
        
        params = (current_user.id,)

        with SQLiteConnection() as cur:
            rows = cur.execute(query, params).fetchall()

        if export_to_excel:

            directory_path: str = None
            try:
                directory_path = select_directory()
            except:
                pass
            
            if directory_path:
                exporter = QueryExporter(query, params, directory_path, "servicetrackers")
                exporter.to_xlsx()

        return rows
