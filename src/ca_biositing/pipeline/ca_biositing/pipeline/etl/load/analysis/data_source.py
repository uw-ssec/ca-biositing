"""
ETL Load: Data Sources

Loads transformed data source information into the DataSource table.
Uses upsert pattern on the id column.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timezone
from prefect import task, get_run_logger
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from ca_biositing.pipeline.utils.engine import get_engine


@task
def load_data_sources(df: pd.DataFrame):
    """
    Upserts data source records into the database.
    """
    try:
        logger = get_run_logger()
    except Exception:
        import logging
        logger = logging.getLogger(__name__)

    if df is None or df.empty:
        logger.info("No data source records to load.")
        return

    logger.info(f"Upserting {len(df)} data source records...")

    try:
        # CRITICAL: Lazy import models inside the task to avoid Docker import hangs
        from ca_biositing.datamodels.models import DataSource

        now = datetime.now(timezone.utc)

        # Filter columns to match the table schema
        table_columns = {c.name for c in DataSource.__table__.columns}
        records = df.replace({np.nan: None}).to_dict(orient='records')

        engine = get_engine()
        with engine.connect() as conn:
            with Session(bind=conn) as session:
                success_count = 0
                for i, record in enumerate(records):
                    # Clean record to only include valid table columns
                    clean_record = {k: v for k, v in record.items() if k in table_columns}

                    # Handle timestamps
                    clean_record['updated_at'] = now
                    if clean_record.get('created_at') is None:
                        clean_record['created_at'] = now

                    # Use upsert pattern (ON CONFLICT DO UPDATE)
                    # Unique constraint is on id
                    stmt = insert(DataSource.__table__).values(**clean_record)

                    # Columns to update if conflict occurs
                    update_cols = {
                        c: stmt.excluded[c]
                        for c in clean_record.keys()
                        if c not in ['id', 'created_at']
                    }

                    if update_cols:
                        stmt = stmt.on_conflict_do_update(
                            index_elements=['id'],
                            set_=update_cols
                        )
                    else:
                        stmt = stmt.on_conflict_do_nothing(
                            index_elements=['id']
                        )

                    session.execute(stmt)
                    success_count += 1

                session.commit()
                logger.info(f"Successfully upserted {success_count} data source records.")

    except Exception as e:
        logger.error(f"Failed to load data source records: {e}")
        raise
