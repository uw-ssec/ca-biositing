import gspread
from gspread.exceptions import SpreadsheetNotFound, APIError
from typing import List, Optional

def get_sheet_names(gsheet_name: str, credentials_path: str) -> Optional[List[str]]:
    """
    Extracts the names of all worksheets in a Google Sheet workbook.

    Args:
        gsheet_name: The name of the Google Sheet.
        credentials_path: The path to the Google Cloud service account credentials JSON file.

    Returns:
        A list of worksheet names, or None if an error occurs.
    """
    try:
        gc = gspread.service_account(filename=credentials_path)
        spreadsheet = gc.open(gsheet_name)
        worksheets = spreadsheet.worksheets()
        return [sheet.title for sheet in worksheets]

    except SpreadsheetNotFound:
        print(f"Error: Spreadsheet '{gsheet_name}' not found.")
        return None
    except APIError as e:
        print(f"Google API Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        gsheet = sys.argv[1]
        creds = sys.argv[2]
        names = get_sheet_names(gsheet, creds)
        if names:
            for name in names:
                print(name)
