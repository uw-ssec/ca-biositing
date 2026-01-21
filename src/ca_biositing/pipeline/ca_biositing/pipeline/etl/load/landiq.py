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
def load_landiq_record(df: pd.DataFrame):
    """
    Upserts Land IQ records into the database.
    """
    print("DEBUG: Entering load_landiq_record task")
    logger = get_run_logger()
    if df is None or df.empty:
        logger.info("No Land IQ record data to load.")
        return

    logger.info(f"Upserting {len(df)} Land IQ records...")

    try:
        from ca_biositing.datamodels.schemas.generated.ca_biositing import LandiqRecord, Polygon
        now = datetime.now(timezone.utc)

        # Get columns that are not primary keys or auto-incrementing
        # We explicitly exclude 'id' because it's a surrogate key that should be handled by the DB
        # However, we MUST include 'record_id' for LandiqRecord even though it's a primary_key
        table_columns = {c.name for c in LandiqRecord.__table__.columns if (not c.primary_key or c.name == 'record_id') and c.name != 'id'}
        poly_columns = {c.name for c in Polygon.__table__.columns if not c.primary_key and c.name != 'id'}
        records = df.replace({np.nan: None}).to_dict(orient='records')

        print("DEBUG: Getting local engine...")
        engine = get_local_engine()
        print(f"DEBUG: load_landiq_record session starting for {len(records)} records")

        with engine.connect() as conn:
            print("DEBUG: Connection established, starting session...")
            with Session(bind=conn, autoflush=False) as session:
                print("DEBUG: load_landiq_record session opened (autoflush=False)")
                for i, record in enumerate(records):
                    if i % 100 == 0:
                        print(f"DEBUG: Processing record {i}...")

                    # 1. Handle Polygon first if geometry is present
                    if 'geometry' in record and record['geometry'] is not None:
                        geom_wkt = record['geometry']
                        if hasattr(geom_wkt, 'wkt'):
                            geom_wkt = geom_wkt.wkt

                        poly_data = {
                            'geom': geom_wkt,
                            'updated_at': now,
                            'created_at': now,
                            'etl_run_id': record.get('etl_run_id'),
                            'lineage_group_id': record.get('lineage_group_id')
                        }
                        clean_poly_data = {k: v for k, v in poly_data.items() if k in poly_columns and k != 'id'}

                        existing_poly = session.query(Polygon).filter_by(geom=geom_wkt).first()
                        if existing_poly:
                            for key, value in clean_poly_data.items():
                                if key not in ['geom', 'created_at']:
                                    setattr(existing_poly, key, value)
                            record['polygon_id'] = existing_poly.id
                        else:
                            new_poly = Polygon(**clean_poly_data)
                            session.add(new_poly)
                            session.flush()
                            record['polygon_id'] = new_poly.id

                    # 2. Handle LandiqRecord
                    clean_record = {k: v for k, v in record.items() if k in table_columns}
                    clean_record['updated_at'] = now
                    if clean_record.get('created_at') is None:
                        clean_record['created_at'] = now

                    existing_record = session.query(LandiqRecord).filter_by(record_id=clean_record.get('record_id')).first()

                    if existing_record:
                        for key, value in clean_record.items():
                            if key not in ['id', 'created_at', 'record_id']:
                                setattr(existing_record, key, value)
                    else:
                        new_record = LandiqRecord(**clean_record)
                        session.add(new_record)

                print("DEBUG: load_landiq_record committing...")
                try:
                    session.commit()
                    print("DEBUG: load_landiq_record commit successful")
                except Exception as commit_error:
                    print(f"DEBUG: Commit failed: {commit_error}")
                    session.rollback()
                    raise
        logger.info("Successfully loaded Land IQ records.")
    except Exception as e:
        logger.error(f"Failed to load Land IQ records: {e}")
        print(f"DEBUG: Error in load_landiq_record: {e}")
        # If it's a foreign key violation, let's see if we can find which record
        raise
