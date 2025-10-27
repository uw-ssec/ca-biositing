import gspread
import pandas as pd
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound, APIError

def gsheet_to_df(gsheet_name: str, worksheet_name: str, credentials_path: str) -> pd.DataFrame:
    """
    Extracts data from a specific tab in a Google Sheet into a pandas DataFrame.

    Args:
        gsheet_name: The name of the Google Sheet.
        worksheet_name: The name of the worksheet/tab.
        credentials_path: The path to the Google Cloud service account credentials JSON file.

    Returns:
        A pandas DataFrame containing the data from the specified worksheet, or None on error.
    """
    try:
        gc = gspread.service_account(filename=credentials_path)

        try:
            spreadsheet = gc.open(gsheet_name)
        except SpreadsheetNotFound:
            print(f"Error: Spreadsheet '{gsheet_name}' not found.")
            print("Please make sure the spreadsheet name is correct and that you have shared it with the service account email.")
            return None

        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except WorksheetNotFound:
            print(f"Error: Worksheet '{worksheet_name}' not found in the spreadsheet.")
            print("Please make sure the worksheet name is correct.")
            return None

        # Get values directly to ensure we get calculated values, not formulas.
        # 'FORMATTED_VALUE' gets the value as you see it in the sheet.
        all_values = worksheet.get_all_values(value_render_option='FORMATTED_VALUE')
        if not all_values:
            return pd.DataFrame() # Return empty DataFrame if sheet is empty

        # Use the first row as header and the rest as data
        df = pd.DataFrame(all_values[1:], columns=all_values[0])

        # De-duplicate columns, keeping the first occurrence
        df = df.loc[:, ~df.columns.duplicated()]

        return df

    except APIError as e:
        print(f"Google API Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == '__main__':
    # This part is for direct execution of this file, which is not the primary use case.
    # The main test logic is in test_gsheet_to_pandas.py
    pass
