import pandas as pd
import numpy as np
from datetime import datetime, timezone
from prefect import task, get_run_logger
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from ca_biositing.pipeline.utils.engine import get_engine

@task
def load_data_template(df: pd.DataFrame):
    """
    Upserts records into the database.

    Template Instructions:
    1. Replace 'YourModel' with the actual SQLModel class.
    2. Update 'index_elements' with the unique constraint column (e.g., 'record_id').
    3. Adjust 'update_dict' exclusions as needed.
    """
    try:
        logger = get_run_logger()
    except Exception:
        import logging
        logger = logging.getLogger(__name__)

    if df is None or df.empty:
        logger.info("No data to load.")
        return

    logger.info(f"Upserting {len(df)} records...")

    try:
        # CRITICAL: Lazy import models inside the task to avoid Docker import hangs
        # from ca_biositing.datamodels.models import YourModel
        from ca_biositing.datamodels.models import Observation as YourModel # Placeholder

        now = datetime.now(timezone.utc)

        # Filter columns to match the table schema
        table_columns = {c.name for c in YourModel.__table__.columns}
        records = df.replace({np.nan: None}).to_dict(orient='records')

        engine = get_engine()
        with engine.connect() as conn:
            with Session(bind=conn) as session:
                for i, record in enumerate(records):
                    # Optional: Add progress logging for larger datasets (from landiq.py)
                    if i > 0 and i % 500 == 0:
                        logger.info(f"Processed {i} records...")

                    # Clean record to only include valid table columns
                    clean_record = {k: v for k, v in record.items() if k in table_columns}

                    # Handle timestamps
                    clean_record['updated_at'] = now
                    if clean_record.get('created_at') is None:
                        clean_record['created_at'] = now

                    # Build Upsert Statement (PostgreSQL specific)
                    stmt = insert(YourModel).values(clean_record)

                    # Define columns to update on conflict
                    # Exclude primary keys and creation timestamps
                    update_dict = {
                        c.name: stmt.excluded[c.name]
                        for c in YourModel.__table__.columns
                        if c.name not in ['id', 'created_at', 'record_id']
                    }

                    upsert_stmt = stmt.on_conflict_do_update(
                        index_elements=['record_id'], # Replace with your unique constraint column
                        set_=update_dict
                    )

                    session.execute(upsert_stmt)

                session.commit()
        logger.info("Successfully upserted records.")
    except Exception as e:
        logger.error(f"Failed to load records: {e}")
        raise
