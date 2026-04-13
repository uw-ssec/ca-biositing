import pandas as pd
import numpy as np
from prefect import task, get_run_logger
from ca_biositing.pipeline.utils.cleaning_functions import cleaning as cleaning_mod
from ca_biositing.pipeline.utils.cleaning_functions import coercion as coercion_mod
from ca_biositing.pipeline.utils.name_id_swap import normalize_dataframes

@task
def transform_fermentation_record(
    raw_df: pd.DataFrame,
    etl_run_id: str | None = None,
    lineage_group_id: str | None = None
) -> pd.DataFrame:
    """
    Transforms raw DataFrame into the FermentationRecord table format.
    Includes cleaning, coercion, and normalization.
    """
    from ca_biositing.datamodels.models import (
        Resource,
        PreparedSample,
        Method,
        Strain,
        Contact,
        Dataset,
        FileObjectMetadata,
        Experiment,
        Equipment,
        DeconVessel
    )
    logger = get_run_logger()
    logger.info("Transforming raw data for FermentationRecord table")

    if raw_df is None or raw_df.empty:
        logger.warning("raw_df is None or empty for FermentationRecord transform")
        return pd.DataFrame()

    # Handle duplicate columns
    raw_df.columns = [str(c).strip() for c in raw_df.columns]
    if "" in raw_df.columns:
        raw_df = raw_df.drop(columns=[""])

    # Pre-clean names to catch normalization-induced duplicates
    raw_df = cleaning_mod.clean_names_df(raw_df)

    # Rename bioconv_method or strain_name to strain if it exists to match normalization expectations
    # We prioritize bioconv_method as it contains the actual strain names in this dataset
    if 'bioconv_method' in raw_df.columns:
        # If both exist, rename strain_name to something else to avoid confusion
        if 'strain_name' in raw_df.columns:
            raw_df = raw_df.rename(columns={'strain_name': 'original_strain_name'})
        raw_df = raw_df.rename(columns={'bioconv_method': 'strain'})
    elif 'strain_name' in raw_df.columns:
        raw_df = raw_df.rename(columns={'strain_name': 'strain'})

    if raw_df.columns.duplicated().any():
        dupes = raw_df.columns[raw_df.columns.duplicated()].unique().tolist()
        logger.warning(f"FermentationRecord: Duplicate columns found and removed: {dupes}")
        raw_df = raw_df.loc[:, ~raw_df.columns.duplicated()]

    logger.info(f"Columns after potential strain rename: {list(raw_df.columns)}")
    if 'strain' in raw_df.columns:
        logger.info(f"Strain column non-null count: {raw_df['strain'].notna().sum()}")
        logger.info(f"Strain column unique values: {raw_df['strain'].unique().tolist()[:5]}")

    # 1. Cleaning & Coercion
    df_copy = raw_df.copy()
    df_copy['dataset'] = 'bioconversion'

    logger.info(f"Raw data columns before cleaning: {list(raw_df.columns)}")

    cleaned_df = cleaning_mod.standard_clean(df_copy)

    if cleaned_df is not None and 'strain' in cleaned_df.columns:
        logger.info(f"Strain column in cleaned_df non-null count: {cleaned_df['strain'].notna().sum()}")
        logger.info(f"Strain column in cleaned_df unique values: {cleaned_df['strain'].unique().tolist()[:5]}")

    if cleaned_df is None:
        logger.error("cleaning_mod.standard_clean returned None for FermentationRecord")
        return pd.DataFrame()

    logger.info(f"Cleaned data columns: {list(cleaned_df.columns)}")

    # Add lineage IDs
    if etl_run_id is not None:
        cleaned_df['etl_run_id'] = etl_run_id
    if lineage_group_id is not None:
        cleaned_df['lineage_group_id'] = lineage_group_id

    coerced_df = coercion_mod.coerce_columns(
        cleaned_df,
        int_cols=['replicate_no'],
        datetime_cols=['created_at', 'updated_at']
    )

    # 2. Normalization
    # Note: method_id in cleaned_df comes from Method_ID in raw data
    # The decon_method and eh_method columns will be created if they exist in cleaned_df,
    # otherwise they'll be skipped by normalize_dataframes and created as all-NA
    normalize_columns = {
        'resource': (Resource, 'name'),
        'prepared_sample': (PreparedSample, 'name'),
        'method_id': (Method, 'name'),
        'decon_method': (Method, 'name'),
        'eh_method': (Method, 'name'),
        'strain': (Strain, 'name'),
        'exp_id': (Experiment, 'name'),
        'analyst_email': (Contact, 'email'),
        'dataset': (Dataset, 'name'),
        'raw_data_url': (FileObjectMetadata, 'uri'),
        'reactor_vessel': (DeconVessel, 'name'),
        'analysis_equipment': (Equipment, 'name')
    }
    logger.info(f"Coerced data columns: {list(coerced_df.columns)}")
    logger.info(f"Normalize columns dict keys: {list(normalize_columns.keys())}")
    logger.info(f"Checking for decon_method: {'decon_method' in coerced_df.columns}")
    logger.info(f"Checking for eh_method: {'eh_method' in coerced_df.columns}")

    normalized_dfs = normalize_dataframes(coerced_df, normalize_columns)
    normalized_df = normalized_dfs[0]

    logger.info(f"Normalized data columns: {list(normalized_df.columns)}")
    logger.info(f"Checking for decon_method_id: {'decon_method_id' in normalized_df.columns}")
    logger.info(f"Checking for eh_method_id: {'eh_method_id' in normalized_df.columns}")

    # 3. Table Specific Mapping
    rename_map = {
        'record_id': 'record_id',
        'replicate_no': 'technical_replicate_no',
        'well_position': 'well_position',
        'qc_result': 'qc_pass',
        'note': 'note',
        'etl_run_id': 'etl_run_id',
        'lineage_group_id': 'lineage_group_id'
    }

    # Handle normalized columns - map them to their target names in FermentationRecord
    column_mapping = {
        'resource': 'resource_id',
        'prepared_sample': 'prepared_sample_id',
        'method_id': 'method_id',  # Keep method_id unchanged
        'decon_method': 'pretreatment_method_id',  # decon_method_id → pretreatment_method_id
        'eh_method': 'eh_method_id',  # eh_method_id → eh_method_id (no change)
        'strain': 'strain_id',
        'exp_id': 'experiment_id',
        'analyst_email': 'analyst_id',
        'dataset': 'dataset_id',
        'raw_data_url': 'raw_data_id',
        'reactor_vessel': 'vessel_id',
        'analysis_equipment': 'analyte_detection_equipment_id'
    }

    for col, target_name in column_mapping.items():
        norm_col = f"{col}_id"
        if norm_col in normalized_df.columns:
            rename_map[norm_col] = target_name
            logger.info(f"Mapping normalized column {norm_col} to {target_name}")

    available_cols = [c for c in rename_map.keys() if c in normalized_df.columns]
    final_rename = {k: v for k, v in rename_map.items() if k in available_cols}

    logger.info(f"Available columns: {available_cols}")
    logger.info(f"Final rename map: {final_rename}")

    try:
        record_df = normalized_df[available_cols].rename(columns=final_rename).copy()

        if 'record_id' in record_df.columns:
            # Filter out placeholder or empty record_id values
            record_df = record_df[~record_df['record_id'].astype(str).str.strip().isin(['-', 'nan', 'None', ''])]
            record_df = record_df.dropna(subset=['record_id'])
        else:
            logger.error("record_id missing from FermentationRecord transform")
            return pd.DataFrame()

        return record_df
    except Exception as e:
        logger.error(f"Error during FermentationRecord transform: {e}")
        return pd.DataFrame()
