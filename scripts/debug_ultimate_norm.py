
import os
import pandas as pd
from prefect import flow, get_run_logger
from ca_biositing.pipeline.etl.extract import ultimate
from ca_biositing.pipeline.utils.cleaning_functions import cleaning as cleaning_mod
from ca_biositing.pipeline.utils.name_id_swap import normalize_dataframes
from ca_biositing.datamodels.models import Parameter

@flow(name="Debug Ultimate Normalization")
def debug_ultimate_norm():
    os.environ['POSTGRES_HOST'] = 'localhost'
    logger = get_run_logger()
    df = ultimate.extract.fn()
    if df is not None:
        cleaned = cleaning_mod.clean_names_df(df)
        logger.info(f"Raw parameters: {cleaned['parameter'].unique().tolist()}")

        # Check Parameter table directly
        from ca_biositing.datamodels.database import get_engine
        from sqlalchemy import text
        engine = get_engine()
        with engine.connect() as conn:
            res = conn.execute(text("SELECT name FROM public.parameter")).scalars().all()
            logger.info(f"DB parameters (sample): {res[:10]}")

        norm_dfs = normalize_dataframes([cleaned], {'parameter': Parameter})
        norm_df = norm_dfs[0]

        logger.info(f"Null parameter_id count: {norm_df['parameter_id'].isna().sum()} out of {len(norm_df)}")
        if norm_df['parameter_id'].isna().any():
            missing = norm_df[norm_df['parameter_id'].isna()]['parameter'].unique().tolist()
            logger.warning(f"Missing parameters in DB: {missing}")

if __name__ == "__main__":
    debug_ultimate_norm()
