import pandas as pd
from prefect import task, get_run_logger
from typing import List
from ca_biositing.pipeline.utils.cleaning_functions import cleaning as cleaning_mod
from ca_biositing.pipeline.utils.cleaning_functions import coercion as coercion_mod
from ca_biositing.pipeline.utils.name_id_swap import normalize_dataframes
from ca_biositing.datamodels.schemas.generated.ca_biositing import *

@task
def transform_observation(raw_dfs: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Transforms raw DataFrames into the Observation table format.
    Includes cleaning, coercion, and normalization.
    """
    logger = get_run_logger()
    logger.info(f"Transforming {len(raw_dfs)} raw dataframes for Observation table")

    # 1. Cleaning & Coercion
    coerced_data = []
    for df in raw_dfs:
        df_copy = df.copy()
        df_copy['dataset'] = 'biocirv'
        cleaned_df = cleaning_mod.standard_clean(df_copy)
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
    for df in coerced_data:
        normalized_df = normalize_dataframes(df, normalize_columns)
        try:
            obs_df = normalized_df[[
                'dataset_id',
                'analysis_type',
                'record_id',
                'parameter_id',
                'value',
                'unit_id',
                'note'
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
