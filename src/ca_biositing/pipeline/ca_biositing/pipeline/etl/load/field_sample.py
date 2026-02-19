import pandas as pd
import numpy as np
from datetime import datetime, timezone
from prefect import task, get_run_logger
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

def get_local_engine():
    import os
    if os.path.exists('/.dockerenv'):
        db_url = "postgresql://biocirv_user:biocirv_dev_password@db:5432/biocirv_db"
    else:
        from ca_biositing.datamodels.config import settings
        db_url = settings.database_url
        if "db:5432" in db_url:
            db_url = db_url.replace("db:5432", "localhost:5432")

    return create_engine(
        db_url,
        pool_size=5,
        max_overflow=0,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 10}
    )

@task
def load_field_sample(df: pd.DataFrame):
    """
    Upserts FieldSample records into the database based on the 'name' column.
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
        logger.info("No FieldSample record data to load.")
        return

    logger.info(f"Upserting {len(df)} FieldSample records...")

    try:
        from ca_biositing.datamodels.models import FieldSample
        now = datetime.now(timezone.utc)
        table_columns = {c.name for c in FieldSample.__table__.columns}

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

                    # Check for existing record by name
                    stmt = select(FieldSample).where(FieldSample.name == name)
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
                        new_fs = FieldSample(**clean_record)
                        session.add(new_fs)

                session.commit()
        logger.info("Successfully upserted FieldSample records.")
    except Exception as e:
        logger.error(f"Failed to load FieldSample records: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise
