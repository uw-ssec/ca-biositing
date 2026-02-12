import pandas as pd
import numpy as np
from datetime import datetime, timezone
from typing import Optional
from prefect import task, get_run_logger
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

def get_local_engine():
    """
    Creates a SQLAlchemy engine based on the environment (Docker vs Local).
    """
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
def load_landiq_resource_mapping(df: pd.DataFrame):
    """
    Upserts LandiqResourceMapping records.
    """
    try:
        logger = get_run_logger()
    except Exception:
        import logging
        logger = logging.getLogger(__name__)

    if df is None or df.empty:
        logger.info("No LandIQ resource mapping data to load.")
        return

    logger.info(f"Upserting {len(df)} LandIQ resource mapping records...")

    try:
        from ca_biositing.datamodels.schemas.generated.ca_biositing import LandiqResourceMapping

        now = datetime.now(timezone.utc)
        table_columns = {c.name for c in LandiqResourceMapping.__table__.columns}
        records = df.replace({np.nan: None}).to_dict(orient='records')

        engine = get_local_engine()
        with engine.connect() as conn:
            with Session(bind=conn) as session:
                for i, record in enumerate(records):
                    if i > 0 and i % 500 == 0:
                        logger.info(f"Processed {i} mapping records...")

                    clean_record = {k: v for k, v in record.items() if k in table_columns}
                    clean_record['updated_at'] = now
                    if clean_record.get('created_at') is None:
                        clean_record['created_at'] = now

                    # Check for existing mapping (unique by landiq_crop_name and resource_id)
                    existing = session.query(LandiqResourceMapping).filter(
                        LandiqResourceMapping.landiq_crop_name == clean_record['landiq_crop_name']
                    ).filter(
                        LandiqResourceMapping.resource_id == clean_record['resource_id']
                    ).first()

                    if existing:
                        for key, value in clean_record.items():
                            if key not in ['id', 'created_at']:
                                setattr(existing, key, value)
                    else:
                        session.add(LandiqResourceMapping(**clean_record))

                session.commit()
        logger.info("Successfully upserted LandIQ resource mapping records.")
    except Exception as e:
        logger.error(f"Failed to load LandIQ resource mapping: {e}")
        raise

@task
def load_resource_availability(df: pd.DataFrame):
    """
    Upserts ResourceAvailability records.
    """
    try:
        logger = get_run_logger()
    except Exception:
        import logging
        logger = logging.getLogger(__name__)

    if df is None or df.empty:
        logger.info("No resource availability data to load.")
        return

    logger.info(f"Upserting {len(df)} resource availability records...")

    try:
        from ca_biositing.datamodels.schemas.generated.ca_biositing import ResourceAvailability

        now = datetime.now(timezone.utc)
        table_columns = {c.name for c in ResourceAvailability.__table__.columns}
        records = df.replace({np.nan: None}).to_dict(orient='records')

        engine = get_local_engine()
        with engine.connect() as conn:
            with Session(bind=conn) as session:
                for i, record in enumerate(records):
                    if i > 0 and i % 500 == 0:
                        logger.info(f"Processed {i} availability records...")

                    clean_record = {k: v for k, v in record.items() if k in table_columns}
                    clean_record['updated_at'] = now
                    if clean_record.get('created_at') is None:
                        clean_record['created_at'] = now

                    # Check for existing availability (unique by resource_id and geoid if applicable,
                    # but for static data we might just use resource_id for now if geoid is null)
                    query = session.query(ResourceAvailability).filter(
                        ResourceAvailability.resource_id == clean_record['resource_id']
                    )

                    if clean_record.get('geoid'):
                        query = query.filter(ResourceAvailability.geoid == clean_record['geoid'])
                    else:
                        query = query.filter(ResourceAvailability.geoid.is_(None))

                    existing = query.first()

                    if existing:
                        for key, value in clean_record.items():
                            if key not in ['id', 'created_at']:
                                setattr(existing, key, value)
                    else:
                        session.add(ResourceAvailability(**clean_record))

                session.commit()
        logger.info("Successfully upserted resource availability records.")
    except Exception as e:
        logger.error(f"Failed to load resource availability: {e}")
        raise
