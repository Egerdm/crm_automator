from google_sheet_updater import GoogleSheetUpdater

def test_google_sheet_updater():
    # Path to your Google service account credentials JSON file
    credentials_file = "automate_credentials.json"
    # Name of your Google Spreadsheet
    spreadsheet_name = "Automate Test"

    # Create an instance of GoogleSheetUpdater
    updater = GoogleSheetUpdater(credentials_file, spreadsheet_name)

    # Test data
    name = "Suzy Rakoci"

    # Add the test email to the Google Sheet
    updater.add_email_to_sheet(name)

if __name__ == "__main__":
    test_google_sheet_updater()