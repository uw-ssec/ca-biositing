
import os
import pandas as pd
from ca_biositing.pipeline.etl.extract.pretreatment_data import extract
from prefect import flow

@flow
def diagnostic_flow():
    print("Extracting data...")
    df = extract()

    if df is None:
        print("Failed to extract data.")
        return

    print(f"Extracted {len(df)} rows.")

    # Check for record_id column (it might be 'Record_id' or 'record_id' depending on sheet)
    col_name = None
    for col in ['Record_id', 'record_id', 'Record ID']:
        if col in df.columns:
            col_name = col
            break

    if col_name is None:
        print(f"Columns found: {df.columns.tolist()}")
        print("Could not find record_id column.")
        return

    print(f"Checking column: {col_name}")

    dupes = df[df.duplicated(subset=[col_name], keep=False)]

    if dupes.empty:
        print("No duplicate record_id values found in raw data.")
    else:
        print(f"Found {len(dupes)} rows with duplicate {col_name} values.")
        print("Duplicate values summary:")
        summary = dupes[col_name].value_counts()
        print(summary)

        print("\nDetail for first few duplicate groups:")
        for val in summary.index[:3]:
            print(f"\n--- Group: {val} ---")
            print(dupes[dupes[col_name] == val][['Parameter', 'Value', 'Unit', 'QC_result']].to_string())

if __name__ == "__main__":
    diagnostic_flow()
