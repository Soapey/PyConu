import csv
from openpyxl import Workbook
from conu.db.SQLiteConnection import SQLiteConnection
from conu.ui.components.Notification import SuccessNotification, ErrorNotification


class QueryExporter():

    def __init__(self, query: str = None, params: tuple = None, directory_path: str = None, file_name_no_extension: str = None) -> None:
        self.query = query
        self.params = params
        self.directory_path = directory_path
        self.file_name = file_name_no_extension

    def to_csv(self):
        try:
            # Execute the query and fetch the resulting data
            with SQLiteConnection() as cur:
                cur.execute(self.query, self.params)
                rows = cur.fetchall()

            # Get the column headers from the cursor description
            headers = [desc[0] for desc in cur.description]

            # Write the data and headers to a CSV file
            file_path = f"{self.directory_path}/{self.file_name}.csv"

            with open(file_path, "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(headers)
                writer.writerows(rows)

            SuccessNotification("Export Successful", [f"Successfully exported to {file_path}."]).show()

        except Exception as e:
            ErrorNotification("Export Failed", [f"Error exporting to CSV: {str(e)}"]).show()

    def to_xlsx(self):
        try:
            # Execute the query and fetch the resulting data
            with SQLiteConnection() as cur:
                cur.execute(self.query, self.params)
                rows = cur.fetchall()

            # Get the column headers from the cursor description
            headers = [desc[0] for desc in cur.description]

            # Create a new workbook and sheet
            workbook = Workbook()
            sheet = workbook.active

            # Write the data and headers to the sheet
            sheet.append(headers)
            for row in rows:
                sheet.append(row)

            # Save the workbook to the specified Excel file path
            file_path = f"{self.directory_path}/{self.file_name}.xlsx"
            workbook.save(file_path)

            SuccessNotification("Export Successful", [f"Successfully exported to {file_path}."]).show()

        except Exception as e:
            ErrorNotification("Export Failed", [f"Error exporting to Excel: {str(e)}"]).show()
