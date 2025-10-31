"""
This module provides utility functions for handling foreign key relationships
in pandas DataFrames, specifically for ETL (Extract, Transform, Load) processes
involving a SQL database managed with SQLModel.

The functions are designed to be generic and reusable for two primary scenarios:
1.  **Replacing Foreign Key IDs with Human-Readable Names:**
    When extracting data, you often get integer IDs (e.g., `biomass_type_id = 1`).
    For analysis or display, you might want the actual name (e.g., `'ag_residue'`).
    The `replace_id_with_name_df` function handles this by mapping IDs to names
    from a reference table.

2.  **Replacing Names with Foreign Key IDs (Get or Create):**
    When loading new data, you might have human-readable names (e.g., a new
    biomass type like `'corn_husks'`). Before inserting this into a table that
    requires a foreign key ID, you need to get the ID for that name. If the name
    doesn't exist in the reference table, it should be created. The
    `replace_name_with_id_df` function automates this "get or create" logic.

These utilities are optimized to minimize database queries by fetching reference
data in bulk and using in-memory lookups (pandas `.map()`), making them
efficient for transforming large datasets.
"""
from typing import Type, TypeVar

import pandas as pd
from sqlmodel import Session, SQLModel

# Define a generic type for SQLModel classes
ModelType = TypeVar("ModelType", bound=SQLModel)


def replace_id_with_name_df(
    db: Session,
    df: pd.DataFrame,
    ref_model: Type[ModelType],
    id_column_name: str,
    name_column_name: str,
) -> pd.DataFrame:
    """
    Replaces an ID column in a DataFrame with names from a reference table.

    Args:
        db: The database session.
        df: The input pandas DataFrame.
        ref_model: The SQLModel class for the reference table.
        id_column_name: The name of the ID column to replace (e.g., "biomass_type_id").
        name_column_name: The name of the corresponding name column in the reference
                          table (e.g., "biomass_type").

    Returns:
        A new DataFrame with the ID column replaced by a name column.
    """
    # Query the reference table to get all records
    ref_records = db.query(ref_model).all()

    # Create a lookup dictionary from ID to name
    id_to_name_map = {
        getattr(record, id_column_name): getattr(record, name_column_name)
        for record in ref_records
    }

    # Create a copy to avoid modifying the original DataFrame
    df_copy = df.copy()

    # Map the ID column to the new name column and drop the old ID column
    df_copy[name_column_name] = df_copy[id_column_name].map(id_to_name_map)
    df_copy = df_copy.drop(columns=[id_column_name])

    return df_copy


def replace_name_with_id_df(
    db: Session,
    df: pd.DataFrame,
    ref_model: Type[ModelType],
    name_column_name: str,
    id_column_name: str,
) -> pd.DataFrame:
    """
    Replaces a name column in a DataFrame with IDs from a reference table,
    creating new entries in the reference table if a name is not found.

    Args:
        db: The database session.
        df: The input pandas DataFrame.
        ref_model: The SQLModel class for the reference table.
        name_column_name: The name of the name column to replace (e.g., "biomass_type").
        id_column_name: The name of the corresponding ID column in the reference
                        table (e.g., "biomass_type_id").

    Returns:
        A new DataFrame with the name column replaced by an ID column.
    """
    # Query the reference table to get all records
    ref_records = db.query(ref_model).all()

    # Create a lookup dictionary from name to ID
    name_to_id_map = {
        getattr(record, name_column_name): getattr(record, id_column_name)
        for record in ref_records
    }

    # Create a copy to avoid modifying the original DataFrame
    df_copy = df.copy()

    # Find unique names in the DataFrame that are not in the reference table
    unique_names_in_df = df_copy[name_column_name].unique()
    new_names = set(unique_names_in_df) - set(name_to_id_map.keys())

    # If there are new names, add them to the reference table
    if new_names:
        for name in new_names:
            # Create a new record and add it to the session
            new_record = ref_model(**{name_column_name: name})
            db.add(new_record)
            db.commit()
            db.refresh(new_record)
            # Update the lookup map with the new ID
            name_to_id_map[name] = getattr(new_record, id_column_name)

    # Map the name column to the new ID column and drop the old name column
    df_copy[id_column_name] = df_copy[name_column_name].map(name_to_id_map)
    df_copy = df_copy.drop(columns=[name_column_name])

    return df_copy
