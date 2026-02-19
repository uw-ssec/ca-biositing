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
    print("DEBUG: transform_observation task execution started")
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
    print("DEBUG: transform_observation models imported")
    """
    Transforms raw DataFrames into the Observation table format.
    Includes cleaning, coercion, and normalization.
    """
    print(f"DEBUG: transform_observation started with {len(raw_dfs)} dfs")
    logger = get_run_logger()
    logger.info(f"Transforming {len(raw_dfs)} raw dataframes for Observation table")

    # 1. Cleaning & Coercion
    coerced_data = []
    for df in raw_dfs:
        df_copy = df.copy()
        df_copy['dataset'] = 'biocirv'
        cleaned_df = cleaning_mod.standard_clean(df_copy)

        if etl_run_id:
            cleaned_df['etl_run_id'] = etl_run_id
        if lineage_group_id:
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
        print(f"DEBUG: Normalizing dataframe #{i+1}")
        normalized_df = normalize_dataframes(df, normalize_columns)
        print(f"DEBUG: Dataframe #{i+1} normalized")
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
