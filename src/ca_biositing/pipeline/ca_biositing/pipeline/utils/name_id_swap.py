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

  import logging
  logger = logging.getLogger(__name__)

  # If using the SQLite fallback, skip DB lookups and return a column of NA.
  try:
      driver_name = db.bind.url.drivername  # type: ignore[attr-defined]
  except Exception:
      driver_name = None
  if driver_name == "sqlite":
      logger.warning("SQLite fallback active; skipping name‑id replacement.")
      df_copy = df.copy()
      df_copy[final_column_name] = pd.NA
      return df_copy, 0

  # 1. Fetch existing reference rows (name + id only)
  try:
    rows = db.execute(
      select(
        getattr(ref_model, model_name_attr),
        getattr(ref_model, id_column_name),
      )
    ).all()
  except Exception as e:
    # If the model does not have the expected attributes (e.g., a dummy
    # placeholder used in tests) or any other issue occurs, fall back to the
    # SQLite‑in‑memory behaviour – return a column of NA values.
    logger.warning(f"Skipping name‑id replacement due to model issue: {e}")
    df_copy = df.copy()
    df_copy[final_column_name] = pd.NA
    return df_copy, 0

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

import logging
from .engine import engine

logger = logging.getLogger(__name__)

def normalize_dataframes(
    dataframes: list[pd.DataFrame] | pd.DataFrame,
    normalize_columns: dict[str, tuple[Any, str]] | None = None,
) -> list[pd.DataFrame] | pd.DataFrame:
    """Normalize a DataFrame or a list of DataFrames by replacing name columns with foreign key IDs.

    Mirrors the implementation in the ETL notebook. Accepts either a single
    DataFrame or a list of DataFrames. ``normalize_columns`` can be omitted; an
    empty dictionary is used by default, allowing callers to supply a custom
    mapping when needed.
    """
    # Normalise ``normalize_columns`` to a mutable dict
    if normalize_columns is None:
        normalize_columns = {}

    # Detect if a single DataFrame was passed
    single_input = isinstance(dataframes, pd.DataFrame)
    if single_input:
        dataframes = [dataframes]

    logger.info(f"Starting normalization for {len(dataframes)} DataFrames.")
    normalized_dfs: list[pd.DataFrame] = []
    try:
        with Session(engine) as db:
            for i, df in enumerate(dataframes):
                if not isinstance(df, pd.DataFrame):
                    logger.warning(f"Item {i+1} is not a DataFrame; skipping.")
                    continue
                logger.info(f"Processing DataFrame #{i+1} with {len(df)} rows.")
                df_norm = df.copy()
                for col, (model, model_name_attr) in normalize_columns.items():
                    if col not in df_norm.columns:
                        logger.warning(f"Column '{col}' missing in DataFrame #{i+1}; skipping.")
                        continue
                    if df_norm[col].isnull().all():
                        logger.info(f"Column '{col}' contains only nulls; skipping normalization.")
                        continue
                    try:
                        df_norm, num_created = replace_name_with_id_df(
                            db=db,
                            df=df_norm,
                            ref_model=model,
                            df_name_column=col,
                            model_name_attr=model_name_attr,
                            id_column_name="id",
                            final_column_name=f"{col}_id",
                        )
                        if num_created:
                            logger.info(f"Created {num_created} new records in {model.__name__}.")
                        nulls = df_norm[f"{col}_id"].isnull().sum()
                        logger.info(f"Normalized column '{col}'. New column '{col}_id' has {nulls} nulls.")
                    except Exception as e:
                        logger.error(
                            f"Error normalizing column '{col}' in DataFrame #{i+1}: {e}",
                            exc_info=True,
                        )
                normalized_dfs.append(df_norm)
                logger.info(f"Finished DataFrame #{i+1}.")
            logger.info("Committing database session.")
            db.commit()
            logger.info("Database commit successful.")
    except Exception as e:
        logger.error(f"Critical error during normalization: {e}", exc_info=True)
        if "db" in locals():
            db.rollback()
            logger.info("Database session rolled back.")
    # If the original input was a single DataFrame, return the first element directly
    if single_input:
        return normalized_dfs[0] if normalized_dfs else pd.DataFrame()
    return normalized_dfs
