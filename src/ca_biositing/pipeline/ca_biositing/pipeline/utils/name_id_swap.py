from typing import Type, TypeVar, Any

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import select

ModelType = TypeVar("ModelType", bound=Any)

def replace_id_with_name_df(
    db: Session,
    df: pd.DataFrame,
    ref_model: Type[ModelType],
    id_column_name: str,
    name_column_name: str,
) -> pd.DataFrame:
    # Fetch reference table rows as mappings
    rows = db.execute(
        select(*ref_model.__table__.columns)
    ).mappings().all()

    # Build ID → name map
    id_to_name_map = {
        row[id_column_name]: row[name_column_name]
        for row in rows
    }

    df_copy = df.copy()
    df_copy[name_column_name] = df_copy[id_column_name].map(id_to_name_map)
    df_copy = df_copy.drop(columns=[id_column_name])

    return df_copy



def replace_name_with_id_df(
    db: Session,
    df: pd.DataFrame,
    ref_model,
    df_name_column: str,
    model_name_attr: str,
    id_column_name: str,
    final_column_name: str,
) -> tuple[pd.DataFrame, int]:
    """
    Replace a DataFrame name column with foreign key IDs from a SQLAlchemy table.
    Creates missing reference records if needed.

    Returns:
        A tuple containing the modified DataFrame and the number of new records created.
    """

    # 1. Fetch existing reference rows (name + id only)
    rows = db.execute(
        select(
            getattr(ref_model, model_name_attr),
            getattr(ref_model, id_column_name),
        )
    ).all()

    name_to_id_map = {name: id_ for name, id_ in rows}

    df_copy = df.copy()

    # 2. Determine which names are new
    unique_names = set(df_copy[df_name_column].dropna().unique())
    new_names = unique_names - set(name_to_id_map.keys())
    num_new_records = len(new_names)

    # 3. Insert missing reference rows
    if new_names:
        for name in new_names:
            new_record = ref_model(**{model_name_attr: name})
            db.add(new_record)

        # Flush to get IDs without ending the transaction
        db.flush()

        # Re-query just-created rows
        refreshed = db.execute(
            select(ref_model).where(
                getattr(ref_model, model_name_attr).in_(new_names)
            )
        ).scalars().all()

        for record in refreshed:
            name_to_id_map[
                getattr(record, model_name_attr)
            ] = getattr(record, id_column_name)

    # 4. Replace name column with ID column
    df_copy[final_column_name] = df_copy[df_name_column].map(name_to_id_map)
    df_copy = df_copy.drop(columns=[df_name_column])

    return df_copy, num_new_records
