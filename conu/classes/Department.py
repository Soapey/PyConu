from conu.db.QueryExporter import QueryExporter
from conu.db.SQLiteConnection import SQLiteConnection
from conu.helpers import select_directory


class Department:
    def __init__(self, id: int = None, name: str = None) -> None:
        self.id = id
        self.name = name

    @classmethod
    def get_listingview_table_data(cls, main_window, export_to_excel = False) -> list[tuple]:

        current_user = main_window.current_user

        if not current_user:
            return

        query = """
                SELECT DISTINCT department.id, department.name
                FROM department
                JOIN userdepartment ON department.id = userdepartment.department_id
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
                exporter = QueryExporter(query, params, directory_path, "departments")
                exporter.to_xlsx()

        return rows
