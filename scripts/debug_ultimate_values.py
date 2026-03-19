
import os
import pandas as pd
from prefect import flow, get_run_logger
from ca_biositing.pipeline.etl.extract import ultimate
from ca_biositing.pipeline.utils.cleaning_functions import cleaning as cleaning_mod

@flow
def debug_ultimate_values():
    os.environ['POSTGRES_HOST'] = 'localhost'
    logger = get_run_logger()
    df = ultimate.extract.fn()
    if df is not None:
        cleaned = cleaning_mod.clean_names_df(df)
        logger.info(f"Ultimate rows: {len(cleaned)}")
        logger.info(f"Null record_id: {cleaned['record_id'].isna().sum()}")
        logger.info(f"Null parameter: {cleaned['parameter'].isna().sum()}")
        logger.info(f"Null value: {cleaned['value'].isna().sum()}")

        # Check non-null rows
        valid = cleaned.dropna(subset=['record_id', 'parameter', 'value'])
        logger.info(f"Rows with record_id, parameter, AND value: {len(valid)}")
        if not valid.empty:
            print(valid[['record_id', 'parameter', 'value']].head())

if __name__ == "__main__":
    debug_ultimate_values()
