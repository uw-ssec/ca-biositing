import pandas as pd
import numpy as np
from datetime import datetime, timezone
from prefect import task, get_run_logger
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

def get_local_engine():
    print("DEBUG: get_local_engine started - using direct engine creation")
    import os
    # Hardcode the URL for the container environment to bypass any settings.py hangs
    if os.path.exists('/.dockerenv'):
        db_url = "postgresql://biocirv_user:biocirv_dev_password@db:5432/biocirv_db"
        print("DEBUG: Using hardcoded Docker DB URL")
    else:
        from ca_biositing.datamodels.config import settings
        db_url = settings.database_url
        if "db:5432" in db_url:
            db_url = db_url.replace("db:5432", "localhost:5432")

    print(f"DEBUG: Creating engine for {db_url}")
    return create_engine(
        db_url,
        pool_size=5,
        max_overflow=0,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 10}
    )

@task
def load_observation(df: pd.DataFrame):
    """
    Upserts observations into the database.
    """
    print("DEBUG: Entering load_observation task")
    from prefect import get_run_logger
    logger = get_run_logger()
    if df is None or df.empty:
        logger.info("No observation data to load.")
        return

    logger.info(f"Upserting {len(df)} observations...")

    try:
        now = datetime.now(timezone.utc)
        records = df.replace({np.nan: None}).to_dict(orient='records')

        from ca_biositing.datamodels.schemas.generated.ca_biositing import Observation
        print("DEBUG: Getting local engine...")
        engine = get_local_engine()
        print(f"DEBUG: load_observation session starting for {len(records)} records")
        from sqlalchemy.orm import Session
        print("DEBUG: Session class imported")
        print("DEBUG: Attempting to open session with engine.connect()...")
        with engine.connect() as conn:
            print("DEBUG: Connection established, starting session...")
            with Session(bind=conn) as session:
                print("DEBUG: load_observation session opened")
                for i, record in enumerate(records):
                    if i % 100 == 0:
                        print(f"DEBUG: Processing record {i}...")
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
                        index_elements=['record_id', 'record_type', 'parameter_id', 'unit_id'],
                        set_=update_dict
                    )
                    session.execute(upsert_stmt)
                print("DEBUG: load_observation committing...")
                session.commit()
                print("DEBUG: load_observation commit successful")
        logger.info("Successfully upserted observations.")
    except Exception as e:
        logger.error(f"Failed to load observations: {e}")
        raise
