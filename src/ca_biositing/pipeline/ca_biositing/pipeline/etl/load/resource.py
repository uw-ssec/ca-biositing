import pandas as pd
import numpy as np
from datetime import datetime, timezone
from prefect import task, get_run_logger
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

def get_local_engine():
    """
    Creates a SQLAlchemy engine based on the environment (Docker vs Local).
    """
    import os
    # Hardcode the URL for the container environment to bypass any settings.py hangs
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
        from ca_biositing.datamodels.schemas.generated.ca_biositing import Resource

        now = datetime.now(timezone.utc)

        # Filter columns to match the table schema
        table_columns = {c.name for c in Resource.__table__.columns}
        records = df.replace({np.nan: None}).to_dict(orient='records')

        engine = get_local_engine()
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
