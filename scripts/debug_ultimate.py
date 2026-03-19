
import os
import pandas as pd
from prefect import flow, get_run_logger
from ca_biositing.pipeline.etl.extract import ultimate
from ca_biositing.pipeline.etl.transform.analysis.observation import transform_observation

@flow(name="Debug Ultimate Transform")
def debug_ultimate_flow():
    os.environ['POSTGRES_HOST'] = 'localhost'
    logger = get_run_logger()
    logger.info("Extracting ultimate data...")
    df = ultimate.extract.fn()
    if df is not None:
        logger.info(f"Extracted {len(df)} rows.")
        logger.info("Columns: " + str(df.columns.tolist()))

        # Manually add analysis_type as the flow does
        df['analysis_type'] = "ultimate analysis"

        logger.info("Running transform_observation...")
        obs_df = transform_observation.fn([df])

        logger.info(f"Transformation produced {len(obs_df)} rows.")
        if len(obs_df) > 0:
            logger.info("Sample output parameters: " + str(obs_df['parameter_id'].unique().tolist()))
        else:
            # Investigate normalization
            from ca_biositing.pipeline.utils.cleaning_functions import cleaning as cleaning_mod
            cleaned_df = cleaning_mod.clean_names_df(df)
            logger.info("Cleaned columns: " + str(cleaned_df.columns.tolist()))
            if 'parameter' in cleaned_df.columns:
                logger.info("Unique parameters in raw: " + str(cleaned_df['parameter'].unique().tolist()))
            else:
                logger.error("'parameter' column missing after cleaning!")
    else:
        logger.error("Extraction returned None.")

if __name__ == "__main__":
    debug_ultimate_flow()
