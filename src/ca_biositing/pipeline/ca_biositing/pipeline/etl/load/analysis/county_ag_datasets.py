"""
ETL Load: County Ag Datasets

Loads transformed dataset information into the Dataset table.
Uses manual check for existing names since no unique constraint exists on 'name'.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timezone
from prefect import task, get_run_logger
from sqlalchemy import text
from sqlalchemy.orm import Session
from ca_biositing.pipeline.utils.engine import get_engine


@task
def load_county_ag_datasets(df: pd.DataFrame):
    """
    Upserts dataset records into the database.
    """
    try:
        logger = get_run_logger()
    except Exception:
        import logging
        logger = logging.getLogger(__name__)

    if df is None or df.empty:
        logger.info("No dataset records to load.")
        return

    logger.info(f"Loading {len(df)} dataset records...")

    try:
        # CRITICAL: Lazy import models inside the task to avoid Docker import hangs
        from ca_biositing.datamodels.models import Dataset

        now = datetime.now(timezone.utc)

        # Filter columns to match the table schema
        table_columns = {c.name for c in Dataset.__table__.columns}
        records = df.replace({np.nan: None}).to_dict(orient='records')

        engine = get_engine()
        with engine.connect() as conn:
            with Session(bind=conn) as session:
                success_count = 0
                for record in records:
                    # Clean record to only include valid table columns
                    clean_record = {k: v for k, v in record.items() if k in table_columns}

                    if not clean_record.get('name'):
                        continue

                    # Handle timestamps
                    clean_record['updated_at'] = now
                    if clean_record.get('created_at') is None:
                        clean_record['created_at'] = now

                    # Manual check for existence by name since no unique constraint exists
                    existing = session.query(Dataset).filter(Dataset.name == clean_record['name']).first()

                    if existing:
                        # Update existing
                        for key, value in clean_record.items():
                            if key not in ['id', 'created_at']:
                                setattr(existing, key, value)
                    else:
                        # Insert new
                        new_ds = Dataset(**clean_record)
                        session.add(new_ds)

                    success_count += 1

                session.commit()
                logger.info(f"Successfully processed {success_count} dataset records.")

    except Exception as e:
        logger.error(f"Failed to load dataset records: {e}")
        raise
