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
    ref_model: Type[ModelType],
    name_column_name: str,
    id_column_name: str,
    final_column_name: str
) -> pd.DataFrame:
    # Fetch reference table rows
    rows = db.execute(
        select(*ref_model.__table__.columns)
    ).mappings().all()

    name_to_id_map = {
        row[name_column_name]: row[id_column_name]
        for row in rows
    }

    df_copy = df.copy()

    unique_names = set(df_copy[name_column_name].dropna().unique())
    new_names = unique_names - set(name_to_id_map.keys())

    if new_names:
        for name in new_names:
            new_record = ref_model(**{name_column_name: name})
            db.add(new_record)

        # Commit once, not per row
        db.commit()

        # Refresh and update lookup
        refreshed = db.execute(
            select(ref_model).where(
                getattr(ref_model, name_column_name).in_(new_names)
            )
        ).scalars().all()

        for record in refreshed:
            name_to_id_map[getattr(record, name_column_name)] = getattr(
                record, id_column_name
            )

    df_copy[id_column_name] = df_copy[name_column_name].map(name_to_id_map)
    df_copy = df_copy.drop(columns=[name_column_name])
    df_copy = df_copy.rename(columns={id_column_name: final_column_name})

    return df_copy
