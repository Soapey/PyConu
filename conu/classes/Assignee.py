from conu.db.QueryExporter import QueryExporter
from conu.db.SQLiteConnection import SQLiteConnection
from conu.helpers import select_directory


class Assignee:
    def __init__(
        self, id: int = None, name: str = None, description: str = None
    ) -> None:
        self.id = id
        self.name = name
        self.description = description

    @classmethod
    def convert_rows_to_instances(cls, rows) -> dict:

        return {
            row[0]: cls(
                row[0],
                row[1],
                row[2],
            )
            for row in rows
        }

    @classmethod
    def get(cls) -> dict:

        with SQLiteConnection() as cur:

            rows = cur.execute(
                """
                SELECT *
                FROM assignee
                """
            ).fetchall()

        return cls.convert_rows_to_instances(rows)

    @classmethod
    def get_listingview_table_data(cls, main_window, export_to_excel = False) -> list[tuple]:

        current_user = main_window.current_user

        if not current_user:
            return

        query = """
                SELECT DISTINCT 
                    assignee.id AS 'ID', 
                    assignee.name AS 'Name', 
                    assignee.description AS 'Description'
                FROM assignee
                JOIN assigneedepartment ON assignee.id = assigneedepartment.assignee_id
                JOIN userdepartment ON assigneedepartment.department_id = userdepartment.department_id
                WHERE userdepartment.user_id = ?;
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
                exporter = QueryExporter(query, params, directory_path, "assignees")
                exporter.to_xlsx()

        return rows
