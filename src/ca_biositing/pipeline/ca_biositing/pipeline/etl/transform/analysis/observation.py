"""
General observation transformation module.
"""
import pandas as pd
from prefect import task, get_run_logger
from typing import List
from ca_biositing.pipeline.utils.cleaning_functions import cleaning as cleaning_mod
from ca_biositing.pipeline.utils.cleaning_functions import coercion as coercion_mod
from ca_biositing.pipeline.utils.name_id_swap import normalize_dataframes
# from ca_biositing.datamodels.models import *

@task
def transform_observation(
    raw_dfs: List[pd.DataFrame],
    etl_run_id: int | None = None,
    lineage_group_id: int | None = None
) -> pd.DataFrame:
    """
    Transforms raw DataFrames into the Observation table format.
    Includes cleaning, coercion, and normalization.
    """
    from ca_biositing.datamodels.models import (
        Resource,
        PreparedSample,
        Method,
        Parameter,
        Unit,
        Contact,
        PrimaryAgProduct,
        Provider,
        Dataset,
    )
    logger = get_run_logger()
    logger.info(f"Transforming {len(raw_dfs)} raw dataframes for Observation table")

    # 1. Cleaning & Coercion
    coerced_data = []
    for i, df in enumerate(raw_dfs):
        if df is None:
            logger.warning(f"DataFrame at index {i} is None. Skipping.")
            continue

        # Check for duplicate columns which cause 'AttributeError: DataFrame object has no attribute str' in cleaning
        # Aggressive cleaning of duplicate/empty columns before processing
        df = df.loc[:, ~df.columns.duplicated()].copy()
        df = df.loc[:, df.columns.notnull()]
        df = df.loc[:, (df.columns != '')]

        # Use shared cleaning functions
        df = cleaning_mod.clean_names_df(df)
        df = cleaning_mod.replace_empty_with_na(df)

        # Basic coercion for Observation fields
        if 'value' in df.columns:
            df = coercion_mod.coerce_columns(df, float_cols=['value'])

        # Add lineage tracking if available
        if etl_run_id is not None:
            df['etl_run_id'] = etl_run_id
        if lineage_group_id is not None:
            df['lineage_group_id'] = lineage_group_id

        coerced_data.append(df)

    # 2. Normalization (Resource, Sample, Parameter, Unit, etc.)
    normalize_columns = {
        'resource': Resource,
        'prepared_sample': PreparedSample,
        'method_id': Method,
        'parameter': Parameter,
        'unit': Unit,
        'analyst_email': (Contact, "email"),
        'main_crop': PrimaryAgProduct,
        'provider': Provider,
        'dataset': Dataset,
    }

    normalized_dfs = normalize_dataframes(coerced_data, normalize_columns)

    # 3. Final Mapping to Observation table
    required_cols = [
        'dataset_id',
        'analysis_type',
        'record_id',
        'parameter_id',
        'value',
        'unit_id',
        'note',
        'etl_run_id',
        'lineage_group_id'
    ]

    observation_data = []
    for i, normalized_df in enumerate(normalized_dfs):
        missing = [c for c in required_cols if c not in normalized_df.columns]
        if missing:
            logger.error(
                f"DataFrame #{i+1} missing columns {missing} for observation transform. "
                f"Available columns: {normalized_df.columns.tolist()}"
            )
            continue
        try:
            obs_df = normalized_df[required_cols].copy().rename(columns={'analysis_type': 'record_type'})

            obs_df = obs_df.dropna(subset=['record_id', 'parameter_id', 'value'])

            # Remove duplicates based on (record_id, record_type, parameter_id) to avoid ON CONFLICT errors
            # Observations table usually has a unique constraint on these three
            if obs_df.duplicated(subset=['record_id', 'record_type', 'parameter_id']).any():
                dupes_count = obs_df.duplicated(subset=['record_id', 'record_type', 'parameter_id']).sum()
                logger.warning(f"Observation: Removing {dupes_count} duplicate observations from transform output.")
                obs_df = obs_df.drop_duplicates(subset=['record_id', 'record_type', 'parameter_id'], keep='first')

            observation_data.append(obs_df)
        except KeyError as e:
            logger.error(f"Missing required column for observation transform: {e}")
            continue

    if not observation_data:
        logger.warning("No observation data produced during transform")
        return pd.DataFrame()

    final_obs_df = pd.concat(observation_data, ignore_index=True)

    # Final check across all source dataframes
    if final_obs_df.duplicated(subset=['record_id', 'record_type', 'parameter_id']).any():
        dupes_count = final_obs_df.duplicated(subset=['record_id', 'record_type', 'parameter_id']).sum()
        logger.warning(f"Observation: Removing {dupes_count} duplicate observations across all source dataframes.")
        final_obs_df = final_obs_df.drop_duplicates(subset=['record_id', 'record_type', 'parameter_id'], keep='first')

    return final_obs_df
