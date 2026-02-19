import pandas as pd
import numpy as np
from datetime import datetime, timezone
from prefect import task, get_run_logger
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
import os

def get_local_engine():
    if os.path.exists('/.dockerenv'):
        db_url = "postgresql://biocirv_user:biocirv_dev_password@db:5432/biocirv_db"
    else:
        from ca_biositing.datamodels.config import settings
        db_url = settings.database_url
        if "db:5432" in db_url:
            db_url = db_url.replace("db:5432", "localhost:5432")
    return create_engine(db_url)

@task
def load(df: pd.DataFrame):
    """
    Loads transformed Billion Ton data into the billion_ton2023_record table.
    Ensures that Place records exist before loading.
    """
    try:
        logger = get_run_logger()
    except Exception:
        import logging
        logger = logging.getLogger(__name__)

    if df is None or df.empty:
        logger.info("No Billion Ton data to load.")
        return

    logger.info(f"Loading {len(df)} Billion Ton records...")

    # CRITICAL: Lazy import models inside the task to avoid Docker import hangs
    from ca_biositing.datamodels.models.external_data.billion_ton import BillionTon2023Record
    from ca_biositing.datamodels.models.places.place import Place

    engine = get_local_engine()
    now = datetime.now(timezone.utc)

    try:
        with engine.connect() as conn:
            with Session(bind=conn) as session:
                # 1. Ensure Places exist (Billion Ton data has county info)
                # Note: This is a simple implementation to avoid FK violations.
                # Ideally, places would be pre-populated or managed by a dedicated ETL.
                unique_geoids = df[['geoid', 'county', 'state_name']].drop_duplicates()

                place_records = []
                for _, row in unique_geoids.iterrows():
                    place_records.append({
                        'geoid': row['geoid'],
                        'county_name': row['county'],
                        'state_name': row['state_name'],
                        'state_fips': row['geoid'][:2],
                        'county_fips': row['geoid'][2:]
                    })

                if place_records:
                    logger.info(f"Ensuring {len(place_records)} Place records exist...")
                    place_stmt = insert(Place).values(place_records)
                    place_stmt = place_stmt.on_conflict_do_nothing(index_elements=['geoid'])
                    session.execute(place_stmt)
                    session.flush()

                # 2. Prepare records for bulk insert
                table_columns = {c.name for c in BillionTon2023Record.__table__.columns if c.name != 'id'}
                records = df.replace({np.nan: None}).to_dict('records')

                etl_run_id = df['etl_run_id'].iloc[0] if 'etl_run_id' in df.columns else None
                lineage_group_id = df['lineage_group_id'].iloc[0] if 'lineage_group_id' in df.columns else None

                clean_records = []
                for record in records:
                    record['created_at'] = now
                    record['updated_at'] = now
                    if etl_run_id is not None:
                        record['etl_run_id'] = int(etl_run_id)
                    if lineage_group_id is not None:
                        record['lineage_group_id'] = int(lineage_group_id)

                    # Cast integer fields explicitly
                    for int_col in ['production', 'btu_ton', 'production_energy_content']:
                        if int_col in record and record[int_col] is not None:
                            record[int_col] = int(float(record[int_col]))

                    clean_record = {k: v for k, v in record.items() if k in table_columns}
                    clean_records.append(clean_record)

                if clean_records:
                    stmt = insert(BillionTon2023Record).values(clean_records)
                    session.execute(stmt)
                    session.commit()

        logger.info(f"Successfully loaded {len(clean_records)} records into BillionTon2023Record.")

    except Exception as e:
        logger.error(f"Failed to load Billion Ton records: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise
