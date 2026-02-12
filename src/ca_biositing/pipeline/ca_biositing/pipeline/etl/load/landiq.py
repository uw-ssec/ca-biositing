import pandas as pd
import numpy as np
from datetime import datetime, timezone
from prefect import task, get_run_logger
from sqlalchemy import create_engine, select, text
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

def bulk_insert_polygons_ignore(session: Session, geoms: list[str], etl_run_id: str = None, lineage_group_id: str = None, dataset_id: int = None):
    """
    Inserts polygons in bulk, ignoring duplicates based on geom.
    """
    if not geoms:
        return

    from ca_biositing.datamodels.schemas.generated.ca_biositing import Polygon
    now = datetime.now(timezone.utc)

    # Ensure IDs are standard Python ints, not numpy.int64
    clean_etl_run_id = int(etl_run_id) if etl_run_id is not None else None
    clean_lineage_group_id = int(lineage_group_id) if lineage_group_id is not None else None

    # Prepare data for bulk insert
    poly_data = [
        {
            'geom': geom,
            'updated_at': now,
            'created_at': now,
            'etl_run_id': clean_etl_run_id,
            'lineage_group_id': clean_lineage_group_id,
            'dataset_id': dataset_id
        }
        for geom in set(geoms) if geom
    ]

    if not poly_data:
        return

    # Use PostgreSQL's ON CONFLICT DO NOTHING
    # Note: The unique constraint is on md5(geom) as per the migration
    stmt = insert(Polygon).values(poly_data)

    # Since we have a unique index on (md5(geom), dataset_id), we target the index
    # to ensure ON CONFLICT DO NOTHING works correctly.
    # The unique index is named 'unique_geom_dataset_md5'
    # Note: We use the functional expression directly to match the index
    # We must use the exact text that matches the index definition
    stmt = stmt.on_conflict_do_nothing(index_elements=[text("(md5(geom))"), "dataset_id"])

    print(f"DEBUG: Executing bulk polygon insert for {len(poly_data)} items")
    try:
        session.execute(stmt)
        session.flush()
    except Exception as e:
        print(f"DEBUG: ERROR during polygon insert: {str(e)}")
        # Fallback: If ON CONFLICT fails, try manual check (slower but safer)
        print("DEBUG: Falling back to manual polygon check...")
        pass

def fetch_polygon_ids_by_geoms(session: Session, geoms: list[str]) -> dict[str, int]:
    """
    Fetches polygon IDs for a list of geometries.
    """
    if not geoms:
        return {}

    from ca_biositing.datamodels.schemas.generated.ca_biositing import Polygon
    unique_geoms = list(set(g for g in geoms if g))

    if not unique_geoms:
        return {}

    # Fetch in chunks if necessary, but for 10k records it should be fine
    # Using text() for the md5(geom) comparison to match the index
    poly_map = {}
    chunk_size = 1000
    for i in range(0, len(unique_geoms), chunk_size):
        chunk = unique_geoms[i:i + chunk_size]
        stmt = select(Polygon.id, Polygon.geom).where(Polygon.geom.in_(chunk))
        print(f"DEBUG: Fetching IDs for chunk of {len(chunk)} geoms")
        result = session.execute(stmt).all()
        for row in result:
            # Ensure we handle potential trailing spaces or formatting differences
            geom_key = row.geom.strip() if hasattr(row.geom, 'strip') else row.geom
            poly_map[geom_key] = row.id

    print(f"DEBUG: Fetched {len(poly_map)} polygon IDs")
    return poly_map

def bulk_upsert_landiq_records(session: Session, records: list[dict]) -> int:
    """
    Upserts LandiqRecords in bulk using ON CONFLICT (record_id) DO UPDATE.
    Returns the number of records processed.
    """
    if not records:
        return 0

    from ca_biositing.datamodels.schemas.generated.ca_biositing import LandiqRecord

    stmt = insert(LandiqRecord).values(records)

    # Get columns to update (all except record_id and created_at)
    update_cols = {
        c.name: c for c in stmt.excluded
        if c.name not in ['id', 'record_id', 'created_at']
    }

    stmt = stmt.on_conflict_do_update(
        index_elements=['record_id'],
        set_=update_cols
    )

    print(f"DEBUG: Executing bulk LandiqRecord upsert for {len(records)} items")
    try:
        result = session.execute(stmt)
        return result.rowcount
    except Exception as e:
        print(f"DEBUG: ERROR during LandiqRecord upsert: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise

@task(persist_result=False)
def load_landiq_record(df: pd.DataFrame):
    """
    Upserts Land IQ records into the database using optimized bulk operations.
    """
    import logging
    import sys

    try:
        logger = get_run_logger()
    except Exception:
        logger = logging.getLogger(__name__)
    if df is None or df.empty:
        logger.info("No Land IQ record data to load.")
        return

    logger.info(f"Upserting {len(df)} Land IQ records...")

    try:
        from ca_biositing.datamodels.schemas.generated.ca_biositing import LandiqRecord, Dataset, PrimaryAgProduct, Polygon
        from ca_biositing.pipeline.utils.lookup_utils import fetch_lookup_ids

        now = datetime.now(timezone.utc)
        engine = get_local_engine()

        with engine.connect() as conn:
            with Session(bind=conn, autoflush=False) as session:
                # 1. Fetch IDs for Crops and Datasets
                crop_cols = ['main_crop', 'secondary_crop', 'tertiary_crop', 'quaternary_crop']
                crop_names = pd.concat([
                    df[col] for col in crop_cols if col in df.columns
                ]).unique().tolist()
                crop_map = fetch_lookup_ids(session, PrimaryAgProduct, crop_names)

                dataset_names = df['dataset_id'].unique().tolist() if 'dataset_id' in df.columns else []
                dataset_map = fetch_lookup_ids(session, Dataset, dataset_names)

                # 2. Bulk Insert Polygons
                geoms = df['geometry'].apply(lambda x: x.wkt if hasattr(x, 'wkt') else x).tolist()
                etl_run_id = df['etl_run_id'].iloc[0] if 'etl_run_id' in df.columns else None
                lineage_group_id = df['lineage_group_id'].iloc[0] if 'lineage_group_id' in df.columns else None
                poly_dataset_id = dataset_map.get(dataset_names[0]) if dataset_names else None

                unique_geoms_list = list(set(geoms))
                bulk_insert_polygons_ignore(session, unique_geoms_list, etl_run_id, lineage_group_id, poly_dataset_id)

                # 3. Fetch IDs for Polygons
                poly_map = {}
                if geoms:
                    unique_geoms = list(set(g.strip() if hasattr(g, 'strip') else g for g in geoms if g))
                    chunk_size = 1000
                    for i in range(0, len(unique_geoms), chunk_size):
                        chunk = unique_geoms[i:i + chunk_size]
                        stmt = select(Polygon.id, Polygon.geom).where(
                            Polygon.geom.in_(chunk),
                            Polygon.dataset_id == poly_dataset_id
                        )
                        result = session.execute(stmt).all()
                        for row in result:
                            poly_map[row.geom.strip() if hasattr(row.geom, 'strip') else row.geom] = row.id

                # 4. Prepare LandiqRecord data (Vectorized)
                table_columns = {c.name for c in LandiqRecord.__table__.columns if c.name != 'id'}
                prep_df = df.copy()
                prep_df['geom_wkt'] = prep_df['geometry'].apply(lambda x: x.wkt if hasattr(x, 'wkt') else str(x)).str.strip()
                prep_df['polygon_id'] = prep_df['geom_wkt'].map(poly_map)

                for col in crop_cols:
                    if col in prep_df.columns:
                        prep_df[col] = prep_df[col].map(crop_map)

                if 'dataset_id' in prep_df.columns:
                    prep_df['dataset_id'] = prep_df['dataset_id'].map(dataset_map)

                prep_df['updated_at'] = now
                prep_df['created_at'] = now

                available_cols = [c for c in prep_df.columns if c in table_columns]
                records_to_upsert = prep_df[available_cols].replace({np.nan: None}).to_dict('records')

                # 5. Bulk Upsert
                upsert_count = bulk_upsert_landiq_records(session, records_to_upsert)
                session.commit()

        logger.info(f"Successfully loaded {upsert_count} Land IQ records.")
    except Exception as e:
        import traceback
        error_msg = f"Failed to load Land IQ records: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        print(f"DEBUG: CRITICAL ERROR in load_landiq_record: {error_msg}")
        raise
