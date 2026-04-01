import pandas as pd
from prefect import task, get_run_logger
from typing import List, Dict, Any, Optional
from ca_biositing.pipeline.utils.cleaning_functions import cleaning as cleaning_mod
from ca_biositing.pipeline.utils.name_id_swap import normalize_dataframes

@task
def transform_experiment(
    raw_dfs: List[pd.DataFrame],
    column_mapping: Optional[Dict[str, str | List[str]]] = None,
    etl_run_id: str | None = None,
    lineage_group_id: str | None = None
) -> pd.DataFrame:
    """
    Transforms raw DataFrames into the Experiment table format.
    Supports flexible mapping to handle different source schemas.
    """
    from ca_biositing.datamodels.models import Contact

    logger = get_run_logger()
    logger.info(f"Transforming {len(raw_dfs)} raw dataframes for Experiment table")

    # Default mapping if none provided
    # Key: target column in Experiment table
    # Value: source column name (or list of possible names)
    if column_mapping is None:
        # Heuristics for common source columns across different pipelines
        column_mapping = {
            'name': ['therm_exp_id', 'experiment_id', 'experiment_guid', 'rx_uuid', 'rxid'],
            'description': ['thermo_exp_title', 'experiment_title', 'description', 'notes'],
            'analyst_email': ['analyst_email', 'contact_email', 'user_email'],
            'exper_start_date': ['experiment_date', 'start_date', 'date']
        }

    processed_dfs = []
    for i, df in enumerate(raw_dfs):
        if df is None or df.empty:
            continue

        df = df.copy()
        # Aggressive pre-cleaning of column names
        df.columns = [str(c).strip() for c in df.columns]

        # Use standard_clean for consistent behavior
        df = cleaning_mod.standard_clean(df)
        if df is None:
            continue

        # Apply mapping
        rename_dict = {}
        for target, sources in column_mapping.items():
            if isinstance(sources, str):
                sources = [sources]
            for src in sources:
                # standard_clean makes everything snake_case
                clean_src = src.lower().replace(' ', '_')
                if clean_src in df.columns:
                    rename_dict[clean_src] = target
                    break

        if not rename_dict:
            logger.warning(f"No columns from mapping found in dataframe #{i+1}")
            continue

        df = df.rename(columns=rename_dict)

        # Ensure identifier 'name' is present
        if 'name' not in df.columns:
            logger.warning(f"'name' (experiment identifier) missing in dataframe #{i+1} after mapping")
            continue

        processed_dfs.append(df)

    if not processed_dfs:
        logger.warning("No experiment data processed after mapping.")
        return pd.DataFrame()

    # 2. Normalization (e.g. analyst_email -> analyst_id)
    normalize_columns = {}
    # Check if any dataframe has analyst_email before adding to normalization
    has_analyst = any('analyst_email' in df.columns for df in processed_dfs)
    if has_analyst:
        normalize_columns['analyst_email'] = (Contact, 'email')

    normalized_dfs = normalize_dataframes(processed_dfs, normalize_columns)

    # 3. Final selection and cleaning
    # Fields from Experiment model + lineage
    target_fields = ['name', 'description', 'analyst_id', 'exper_start_date', 'etl_run_id', 'lineage_group_id']

    experiment_records = []
    for df in normalized_dfs:
        # Map analyst_email_id to analyst_id if it exists
        if 'analyst_email_id' in df.columns:
            df = df.rename(columns={'analyst_email_id': 'analyst_id'})

        # Ensure lineage is set
        df['etl_run_id'] = etl_run_id
        df['lineage_group_id'] = lineage_group_id

        # Select only target fields that are present
        available = [c for c in target_fields if c in df.columns]
        record_df = df[available].copy()

        experiment_records.append(record_df)

    if not experiment_records:
        return pd.DataFrame()

    final_df = pd.concat(experiment_records, ignore_index=True)

    # Identifier cleaning: unique, non-null, trimmed, lowercased
    final_df['name'] = final_df['name'].astype(str).str.strip().str.lower()
    final_df = final_df[~final_df['name'].isin(['-', 'nan', 'none', ''])]
    final_df = final_df.dropna(subset=['name'])
    final_df = final_df.drop_duplicates(subset=['name'])

    return final_df
