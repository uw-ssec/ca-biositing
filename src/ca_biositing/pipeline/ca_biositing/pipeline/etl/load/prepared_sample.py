import pandas as pd
import numpy as np
from datetime import datetime, timezone
from prefect import task, get_run_logger
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from ca_biositing.pipeline.utils.engine import engine

def get_local_engine():
    """
    Returns the shared SQLAlchemy engine instance.
    """
    return engine

@task
def load_prepared_sample(df: pd.DataFrame):
    """
    Upserts PreparedSample records into the database based on the 'name' column.
    """
    import logging
    import sys
    try:
        logger = get_run_logger()
    except Exception:
        logger = logging.getLogger("prefect.task_runs")
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

    if df is None or df.empty:
        logger.info("No PreparedSample record data to load.")
        return

    logger.info(f"Upserting {len(df)} PreparedSample records...")

    try:
        # CRITICAL: Lazy import models inside the task to avoid Docker import hangs
        from ca_biositing.datamodels.models import PreparedSample

        now = datetime.now(timezone.utc)
        table_columns = {c.name for c in PreparedSample.__table__.columns}

        # Replace NaN with None for database compatibility
        records = df.replace({np.nan: None}).to_dict(orient='records')

        engine = get_local_engine()
        with engine.connect() as conn:
            with Session(bind=conn) as session:
                for record in records:
                    name = record.get('name')
                    if not name:
                        logger.warning("Skipping record with missing 'name'.")
                        continue

                    # Check for existing record by name (pandas-based logic equivalent in SQL)
                    stmt = select(PreparedSample).where(PreparedSample.name == name)
                    existing_record = session.execute(stmt).scalar_one_or_none()

                    clean_record = {k: v for k, v in record.items() if k in table_columns}
                    clean_record['updated_at'] = now

                    if existing_record:
                        # Update existing record
                        for key, value in clean_record.items():
                            if key not in ['id', 'created_at']:
                                setattr(existing_record, key, value)
                    else:
                        # Create new record
                        if clean_record.get('created_at') is None:
                            clean_record['created_at'] = now
                        new_ps = PreparedSample(**clean_record)
                        session.add(new_ps)

                session.commit()
        logger.info("Successfully upserted PreparedSample records.")
    except Exception as e:
        logger.error(f"Failed to load PreparedSample records: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise
