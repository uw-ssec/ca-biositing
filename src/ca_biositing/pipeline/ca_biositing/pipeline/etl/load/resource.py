import pandas as pd
import numpy as np
from datetime import datetime, timezone
from prefect import task, get_run_logger
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from ca_biositing.pipeline.utils.engine import get_engine

@task
def load_resource(df: pd.DataFrame):
    """
    Upserts resource records into the database.
    """
    try:
        logger = get_run_logger()
    except Exception:
        import logging
        logger = logging.getLogger(__name__)

    if df is None or df.empty:
        logger.info("No data to load.")
        return

    logger.info(f"Upserting {len(df)} resource records...")

    try:
        # CRITICAL: Lazy import models inside the task to avoid Docker import hangs
        from ca_biositing.datamodels.models import Resource

        now = datetime.now(timezone.utc)

        # Filter columns to match the table schema
        table_columns = {c.name for c in Resource.__table__.columns}
        records = df.replace({np.nan: None}).to_dict(orient='records')

        engine = get_engine()
        with engine.connect() as conn:
            with Session(bind=conn) as session:
                for i, record in enumerate(records):
                    if i > 0 and i % 500 == 0:
                        logger.info(f"Processed {i} records...")

                    # Clean record to only include valid table columns
                    clean_record = {k: v for k, v in record.items() if k in table_columns}

                    # Handle timestamps
                    clean_record['updated_at'] = now
                    if clean_record.get('created_at') is None:
                        clean_record['created_at'] = now

                    # Manual Check-and-Update (since 'name' lacks a unique constraint)
                    existing_record = session.query(Resource).filter(Resource.name == clean_record['name']).first()

                    if existing_record:
                        # Update existing record
                        for key, value in clean_record.items():
                            if key not in ['id', 'created_at']:
                                setattr(existing_record, key, value)
                    else:
                        # Insert new record
                        new_resource = Resource(**clean_record)
                        session.add(new_resource)

                session.commit()
        logger.info("Successfully upserted resource records.")
    except Exception as e:
        logger.error(f"Failed to load resource records: {e}")
        raise
