
import os
import pandas as pd
from prefect import flow, get_run_logger
from ca_biositing.pipeline.etl.extract import cmpana
from ca_biositing.pipeline.etl.transform.analysis.observation import transform_observation

@flow
def debug_cmpana():
    os.environ['POSTGRES_HOST'] = 'localhost'
    logger = get_run_logger()
    df = cmpana.extract.fn()
    if df is not None:
        logger.info(f"CMPANA columns: {df.columns.tolist()}")
        df['analysis_type'] = "compositional analysis"
        obs_df = transform_observation.fn([df])
        logger.info(f"Produced {len(obs_df)} observations")
        if not obs_df.empty:
            print(obs_df.head())
        else:
            # Check why
            from ca_biositing.pipeline.utils.cleaning_functions import cleaning as cleaning_mod
            cleaned = cleaning_mod.clean_names_df(df)
            logger.info(f"Cleaned columns: {cleaned.columns.tolist()}")
            logger.info(f"Null values in 'value': {cleaned['value'].isna().sum() if 'value' in cleaned.columns else 'N/A'}")
            logger.info(f"Null values in 'parameter': {cleaned['parameter'].isna().sum() if 'parameter' in cleaned.columns else 'N/A'}")

if __name__ == "__main__":
    debug_cmpana()
