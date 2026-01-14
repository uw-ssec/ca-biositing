import pandas as pd
from pydrive2.auth import GoogleAuth, AuthenticationError
from pydrive2.drive import GoogleDrive
from pydrive2.files import ApiRequestError
import zipfile
import geopandas as gpd
import os

def gdrive_to_df(file_name: str, mime_type: str, credentials_path: str, dataset_folder: str) -> pd.DataFrame | gpd.GeoDataFrame:
    """
    Extracts data from a CSV, ZIP, or GEOJSON file into a pandas DataFrame.

    Args:
        file_name: The name of the requested file.
        mime_type: The MIME type - according to https://mime-type.com/
        credentials_path: The path to the Google Cloud service account credentials JSON file.
        dataset_folder: the folder where the extracted file is stored.

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
            file_entries = drive.ListFile({"q": f"title = '{file_name}' and mimeType= '{mime_type}'"}).GetList()
            if len(file_entries) == 0:
                raise FileNotFoundError(f"Error: File '{file_name}' not found. \n Please make sure the name and mimeType is correct and that you have shared it with the service account email.")
                return None
            else:
                file_entry = file_entries[0]
            file = drive.CreateFile({'id': file_entry['id']})
            file.GetContentFile(dataset_folder + file_name) # Download file
        except ApiRequestError:
            print(f"An unexpected error occurred: {e}")
            return None

        # read csv if file is csv
        if mime_type == "text/csv":
            df = pd.read_csv(dataset_folder + file_name)

        # extract from zip if file is zip
        # note: THIS CODE ASSUMES THAT THE ZIP ONLY CONTAINS ONE CSV FILE
        elif mime_type == "application/zip":

            # note: THIS CODE ASSUMES THAT THE CSV FILE HAS THE SAME NAME AS THE ZIP FILE
            csv_name = file_name[:-4] + ".csv"

            with zipfile.ZipFile(dataset_folder + file_name,"r") as zip_ref:
                zip_ref.extractall(dataset_folder)
            df = pd.read_csv(dataset_folder + csv_name)

        elif mime_type == "application/geo+json":
            df = gpd.read_file(dataset_folder + file_name)
        else:
            raise Exception("Can't handle this MIME type. Sorry.")

        # De-duplicate columns, keeping the first occurrence
        df = df.loc[:, ~df.columns.duplicated()]

        return df

    except AuthenticationError as e:
        print(f"Google Authentication Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == '__main__':
    # This part is for direct execution of this file, which is not the primary use case.
    # The main test logic is in test_gsheet_to_pandas.py
    pass
