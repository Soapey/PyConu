from dataclasses import dataclass
from datetime import datetime, date
from conu.db.SQLiteConnection import SQLiteConnection
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem
from conu.db.helpers import select_by_attrs_dict, format_nullable_database_date
from conu.classes.Item import Item


@dataclass
class ServiceTracker:
    id: int
    item_id: int
    units_calibration_date: date
    current_units: int
    average_units_per_day: int
    service_due_units: int
    service_interval: int

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
            entites = list(cls.select_by_attr_dict().values())

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
    def get_by_user_departments(cls, user_id):

        with SQLiteConnection() as cur:

            rows = cur.execute(
                """
                SELECT 
                    * 
                FROM 
                    servicetracker 
                WHERE 
                    servicetracker.item_id IN (SELECT itemdepartment.item_id FROM itemdepartment WHERE itemdepartment.department_id IN (SELECT userdepartment.department_id FROM userdepartment WHERE userdepartment.user_id = ?))
                """,
                (user_id,),
            ).fetchall()

        return cls.convert_rows_to_instances(rows)
