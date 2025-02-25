import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from gspread_formatting import CellFormat, format_cell_range, NumberFormat

class GoogleSheetUpdater:
    def __init__(self, credentials_file, spreadsheet_name):
        self.credentials_file = credentials_file
        self.spreadsheet_name = spreadsheet_name
        self.client = self.authenticate_google_sheets()
        self.sheet = self.client.open(spreadsheet_name).sheet1

    def authenticate_google_sheets(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
        client = gspread.authorize(creds)
        return client

    def add_email_to_sheet(self, name, status_message):
        current_date = datetime.now().strftime("%d.%m.%Y")
        row = ["", current_date, name, status_message, "", "", ""]
        self.sheet.append_row(row)
        print(f"✅ E-posta Google Sheet'e eklendi: {name}")

        # Get the index of the last row
        last_row_index = len(self.sheet.get_all_values())

        # Apply date format to the date cell
        date_format = CellFormat(
            numberFormat=NumberFormat(type="DATE", pattern="dd.MM.yyyy")
        )
        format_cell_range(self.sheet, f"B{last_row_index}", date_format)

    def list_spreadsheets(self):
        spreadsheets = self.client.openall()
        for sheet in spreadsheets:
            print(sheet.title)

# Test the class
if __name__ == "__main__":
    credentials_file = "automate_credentials.json"
    spreadsheet_name = "Automate Test"
    updater = GoogleSheetUpdater(credentials_file, spreadsheet_name)
    updater.add_email_to_sheet("Suzan Rakıcı", "mesaj gönderilmedi")