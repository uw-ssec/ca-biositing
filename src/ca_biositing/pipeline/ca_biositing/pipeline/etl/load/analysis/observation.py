import pandas as pd
import numpy as np
from datetime import datetime, timezone
from prefect import task, get_run_logger
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from ca_biositing.datamodels.config import settings
from ca_biositing.datamodels.schemas.generated.ca_biositing import Observation

def get_local_engine():
    db_url = settings.database_url
    if "@db:" in db_url:
        db_url = db_url.replace("@db:", "@localhost:")
    elif "db:5432" in db_url:
        db_url = db_url.replace("db:5432", "localhost:5432")
    return create_engine(db_url)

@task
def load_observation(df: pd.DataFrame):
    """
    Upserts observations into the database.
    """
    logger = get_run_logger()
    if df is None or df.empty:
        logger.info("No observation data to load.")
        return

    logger.info(f"Upserting {len(df)} observations...")

    try:
        now = datetime.now(timezone.utc)
        records = df.replace({np.nan: None}).to_dict(orient='records')

        engine = get_local_engine()
        with Session(engine) as session:
            for record in records:
                record['updated_at'] = now
                if record.get('created_at') is None:
                    record['created_at'] = now

                stmt = insert(Observation).values(record)
                update_dict = {
                    c.name: stmt.excluded[c.name]
                    for c in Observation.__table__.columns
                    if c.name not in ['id', 'created_at', 'record_id']
                }
                upsert_stmt = stmt.on_conflict_do_update(
                    index_elements=['record_id'],
                    set_=update_dict
                )
                session.execute(upsert_stmt)
            session.commit()
        logger.info("Successfully upserted observations.")
    except Exception as e:
        logger.error(f"Failed to load observations: {e}")
        raise
