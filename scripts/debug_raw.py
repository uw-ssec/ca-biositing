
import os
import pandas as pd
from prefect import flow, get_run_logger
from ca_biositing.pipeline.etl.extract import ultimate, cmpana, icp
from ca_biositing.pipeline.utils.cleaning_functions import cleaning as cleaning_mod

@flow(name="Debug Raw Data")
def debug_raw_flow():
    os.environ['POSTGRES_HOST'] = 'localhost'
    logger = get_run_logger()

    for name, extractor in [("Ultimate", ultimate), ("Compositional", cmpana), ("ICP", icp)]:
        logger.info(f"Checking {name}...")
        df = extractor.extract.fn()
        if df is not None:
            logger.info(f"{name} columns: {df.columns.tolist()}")
            cleaned = cleaning_mod.clean_names_df(df)
            logger.info(f"{name} cleaned columns: {cleaned.columns.tolist()}")

            if 'parameter' in cleaned.columns:
                logger.info(f"{name} unique parameters: {cleaned['parameter'].unique().tolist()}")
            else:
                logger.error(f"{name} MISSING 'parameter' column!")

            if 'value' in cleaned.columns:
                logger.info(f"{name} has 'value' column.")
            else:
                logger.error(f"{name} MISSING 'value' column!")
        else:
            logger.error(f"{name} extraction failed!")

if __name__ == "__main__":
    debug_raw_flow()
