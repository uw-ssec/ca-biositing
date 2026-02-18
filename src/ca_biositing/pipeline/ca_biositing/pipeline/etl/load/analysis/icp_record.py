import pandas as pd
import numpy as np
from datetime import datetime, timezone
from prefect import task, get_run_logger
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
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
def load_icp_record(df: pd.DataFrame):
    """
    Upserts ICP records into the database.
    """
    logger = get_run_logger()
    if df is None or df.empty:
        logger.info("No ICP record data to load.")
        return

    logger.info(f"Upserting {len(df)} ICP records...")

    try:
        from ca_biositing.datamodels.models import IcpRecord
        now = datetime.now(timezone.utc)
        table_columns = {c.name for c in IcpRecord.__table__.columns}
        records = df.replace({np.nan: None}).to_dict(orient='records')

        engine = get_local_engine()
        with engine.connect() as conn:
            with Session(bind=conn) as session:
                for record in records:
                    clean_record = {k: v for k, v in record.items() if k in table_columns}
                    clean_record['updated_at'] = now
                    if clean_record.get('created_at') is None:
                        clean_record['created_at'] = now

                    stmt = insert(IcpRecord).values(clean_record)
                    update_dict = {
                        c.name: stmt.excluded[c.name]
                        for c in IcpRecord.__table__.columns
                        if c.name not in ['id', 'created_at', 'record_id']
                    }
                    upsert_stmt = stmt.on_conflict_do_update(
                        index_elements=['record_id'],
                        set_=update_dict
                    )
                    session.execute(upsert_stmt)
                session.commit()
        logger.info("Successfully upserted ICP records.")
    except Exception as e:
        logger.error(f"Failed to load ICP records: {e}")
        raise
