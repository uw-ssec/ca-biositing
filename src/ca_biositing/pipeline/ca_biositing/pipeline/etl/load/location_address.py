import pandas as pd
import numpy as np
from datetime import datetime, timezone
from prefect import task, get_run_logger
from sqlalchemy import select
from sqlalchemy.orm import Session
from ca_biositing.pipeline.utils.engine import engine, get_engine

@task
def load_location_address(df: pd.DataFrame):
    """
    Upserts LocationAddress records into the database.
    Maps generic location names (like counties) to geography_ids during load.
    """
    import logging
    import sys
    try:
        logger = get_run_logger()
    except Exception:
        logger = logging.getLogger("prefect.task_runs")
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

    if df is None or df.empty:
        logger.info("No LocationAddress record data to load.")
        return

    logger.info(f"Upserting {len(df)} LocationAddress records...")

    try:
        from ca_biositing.datamodels.models import LocationAddress, Place
        now = datetime.now(timezone.utc)
        table_columns = {c.name for c in LocationAddress.__table__.columns}

        # Replace NaN with None for database compatibility
        records = df.replace({np.nan: None}).to_dict(orient='records')

        with Session(get_engine()) as session:
            # Prepare geography mapping
            places = session.execute(select(Place.geoid, Place.county_name)).all()
            county_to_geoid = {p.county_name.lower(): p.geoid for p in places if p.county_name}

            def get_geoid(val):
                if not val: return '06000'
                val_clean = str(val).strip().lower()
                if val_clean in county_to_geoid: return county_to_geoid[val_clean]
                if f"{val_clean} county" in county_to_geoid: return county_to_geoid[f"{val_clean} county"]
                return '06000'

            for record in records:
                # Map raw sampling_location to geoid
                raw_loc = record.get('sampling_location')
                geography_id = get_geoid(raw_loc)

                address_line1 = record.get('address_line1')
                city = record.get('city')

                # Check for existing record
                stmt = select(LocationAddress).where(LocationAddress.geography_id == geography_id)
                if address_line1:
                    stmt = stmt.where(LocationAddress.address_line1 == address_line1)
                else:
                    stmt = stmt.where(LocationAddress.address_line1.is_(None))

                if city:
                    stmt = stmt.where(LocationAddress.city == city)
                else:
                    stmt = stmt.where(LocationAddress.city.is_(None))

                # Fetch only one to avoid MultipleResultsFound
                existing_record = session.execute(stmt).scalars().first()

                clean_record = {k: v for k, v in record.items() if k in table_columns}
                clean_record['geography_id'] = geography_id
                clean_record['updated_at'] = now

                if existing_record:
                    # Update existing record
                    for key, value in clean_record.items():
                        if key not in ['id', 'created_at']:
                            setattr(existing_record, key, value)
                else:
                    # Create new record
                    if clean_record.get('created_at') is None:
                        clean_record['created_at'] = now
                    new_la = LocationAddress(**clean_record)
                    session.add(new_la)

            session.commit()
        logger.info("Successfully upserted LocationAddress records.")
    except Exception as e:
        logger.error(f"Failed to load LocationAddress records: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise
