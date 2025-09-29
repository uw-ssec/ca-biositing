"""
ETL Load Template
---

This module provides a template for loading transformed data into the database.

To use this template:
1.  Copy this file to the appropriate subdirectory in `src/etl/load/`.
    For example: `src/etl/load/new_module/new_data.py`
2.  Import the correct SQLModel class from `src/models/`.
3.  Update the placeholder variables and logic in the `load` function.
"""

import pandas as pd
from sqlmodel import Session, select
from src.database import engine

# --- MODEL IMPORT ---
# TODO: Import the specific SQLModel class that corresponds to the data being loaded.
# from src.models.your_model import YourModelClass
from src.models.biomass import PrimaryProduct # Placeholder, replace with your model


def load(df: pd.DataFrame):
    """
    Loads the transformed data into the corresponding database table.

    This function serves as the 'Load' step in an ETL pipeline.

    Args:
        df (pd.DataFrame): The transformed data ready for database insertion.
    """
    # --- CONFIGURATION ---
    # TODO: Replace `YourModelClass` with the actual name of your imported model.
    YourModelClass = PrimaryProduct # Placeholder, replace with your model

    # TODO: Replace `unique_db_column` with the actual column name in your DB model
    # that should be used for checking for existing records.
    unique_db_column = "primary_product_name" # Placeholder

    # TODO: Replace `df_column_name` with the corresponding column name in the DataFrame.
    df_column_name = "primary_product_name" # Placeholder

    # --- 1. Input Validation ---
    if df is None or df.empty:
        print("No data to load. Skipping database insertion.")
        return

    if df_column_name not in df.columns:
        print(f"Error: Column '{df_column_name}' not found in the DataFrame. Aborting load.")
        return

    print(f"Attempting to load {len(df)} records into the database...")

    # --- 2. Database Loading ---
    with Session(engine) as session:
        # Get existing records from the database to prevent duplicates
        statement = select(getattr(YourModelClass, unique_db_column))
        existing_records = session.exec(statement).all()
        existing_ids = set(existing_records)

        records_to_add = []
        for index, row in df.iterrows():
            record_id = row[df_column_name]
            if record_id not in existing_ids:
                # --- DATA MAPPING ---
                # TODO: Create an instance of your model, mapping DataFrame columns
                # to the model's attributes.
                new_record = YourModelClass(
                    # example_attribute=row['dataframe_column_name'],
                    primary_product_name=row['primary_product_name'] # Placeholder
                )
                records_to_add.append(new_record)
                # Add the new ID to our set to handle duplicates within the DataFrame
                existing_ids.add(record_id)

        if records_to_add:
            session.add_all(records_to_add)
            session.commit()
            print(f"Successfully committed {len(records_to_add)} new records to the database.")
        else:
            print("No new records to add. All records already exist in the database.")
