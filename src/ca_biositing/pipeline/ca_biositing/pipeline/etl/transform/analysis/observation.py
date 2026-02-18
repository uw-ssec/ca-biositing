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
    etl_run_id: int = None,
    lineage_group_id: int = None
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
        # Aggressive cleaning of duplicate/empty columns before processing
        # This handles cases like 'Upload_status' vs 'Upload Status' and hidden empty columns
        # First, strip whitespace and drop purely empty columns
        df = df.copy()
        df.columns = [str(c).strip() for c in df.columns]
        if "" in df.columns:
            df = df.drop(columns=[""])

        # Apply name cleaning EARLY to catch duplicates that arise from normalization (e.g. 'Upload Status' -> 'upload_status')
        df = cleaning_mod.clean_names_df(df)

        if df.columns.duplicated().any():
            dupes = df.columns[df.columns.duplicated()].unique().tolist()
            logger.warning(f"DataFrame at index {i} has duplicate columns after name cleaning: {dupes}. Keeping first occurrence.")
            # Keep only the first occurrence of each column name
            df = df.loc[:, ~df.columns.duplicated()]

        df_copy = df.copy()
        df_copy['dataset'] = 'biocirv'

        logger.info(f"Cleaning DataFrame #{i+1} with columns: {df_copy.columns.tolist()}")
        # standard_clean will call clean_names again, but it's now idempotent and safe
        cleaned_df = cleaning_mod.standard_clean(df_copy)

        if etl_run_id is not None:
            cleaned_df['etl_run_id'] = etl_run_id
        if lineage_group_id is not None:
            cleaned_df['lineage_group_id'] = lineage_group_id

        coerced_df = coercion_mod.coerce_columns(
            cleaned_df,
            int_cols=['repl_no'],
            float_cols=['value'],
            datetime_cols=['created_at', 'updated_at']
        )
        coerced_data.append(coerced_df)

    # 2. Normalization
    normalize_columns = {
        'resource': (Resource, 'name'),
        'prepared_sample': (PreparedSample, 'name'),
        'preparation_method': (Method, 'name'),
        'parameter': (Parameter, 'name'),
        'unit': (Unit, 'name'),
        'sample_unit': (Unit, 'name'),
        'analyst_email': (Contact, 'email'),
        'primary_ag_product': (PrimaryAgProduct, 'name'),
        'provider_code': (Provider, 'codename'),
        'dataset': (Dataset, 'name')
    }

    observation_data = []
    for i, df in enumerate(coerced_data):
        normalized_df = normalize_dataframes(df, normalize_columns)
        try:
            obs_df = normalized_df[[
                'dataset_id',
                'analysis_type',
                'record_id',
                'parameter_id',
                'value',
                'unit_id',
                'note',
                'etl_run_id',
                'lineage_group_id'
            ]].copy().rename(columns={'analysis_type': 'record_type'})

            obs_df = obs_df.dropna(subset=['record_id', 'parameter_id', 'value'])
            observation_data.append(obs_df)
        except KeyError as e:
            logger.error(f"Missing required column for observation transform: {e}")
            continue

    if not observation_data:
        logger.warning("No observation data produced during transform")
        return pd.DataFrame()

    return pd.concat(observation_data, ignore_index=True)
