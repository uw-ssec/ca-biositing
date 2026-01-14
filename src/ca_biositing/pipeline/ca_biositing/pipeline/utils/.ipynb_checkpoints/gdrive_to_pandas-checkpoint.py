import pandas as pd
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def gdrive_to_df(file_name: str, credentials_path: str) -> pd.DataFrame:
    """
    Extracts data from a CSV or GEOJSON into a pandas DataFrame.

    Args:
        file_name: The name of the requested file.
        credentials_path: The path to the Google Cloud service account credentials JSON file.

    Returns:
        A pandas DataFrame containing the data from the specified worksheet, or None on error.
    """
    try:
        settings = {
                "client_config_backend": "service",
                "service_config": {
                    "client_json_file_path": credentials_path,
                }
            }
        # Create instance of GoogleAuth
        gauth = GoogleAuth(settings=settings)
        gauth.ServiceAuth()
        drive = GoogleDrive(gauth)

        try:
            file_list = drive.ListFile().GetList()
            print(file_list)
        except SpreadsheetNotFound:
            print(f"Error: Spreadsheet '{gsheet_name}' not found.")
            print("Please make sure the spreadsheet name is correct and that you have shared it with the service account email.")
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
