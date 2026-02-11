# File: src/ca_biositing/pipeline/etl/load/usda/usda_census_survey.py
"""
USDA Census/Survey Data Load
---
Loads transformed USDA data into database with atomic dataset creation + linking.
"""

from typing import Optional
import pandas as pd
from datetime import datetime, timezone
from prefect import task, get_run_logger
from sqlalchemy import create_engine, text, insert
from sqlalchemy.dialects.postgresql import insert as pg_insert


def get_local_engine():
    """Creates a SQLAlchemy engine, avoiding settings.py hangs in Docker."""
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
def load(
    transformed_df: Optional[pd.DataFrame],
    etl_run_id: int = None,
    lineage_group_id: int = None
) -> bool:
    """
    Load transformed USDA data with integrated dataset creation and linking.

    Implements 3-level deduplication:
    - Level 1: Skip if exists in database
    - Level 2: Skip if seen earlier in this batch
    - Level 3: PostgreSQL ON CONFLICT for final safety
    """
    logger = get_run_logger()

    if transformed_df is None or len(transformed_df) == 0:
        logger.warning("No data to load")
        return True

    logger.info(f"Starting load of {len(transformed_df)} records...")

    try:
        # --- LAZY IMPORT ---
        from ca_biositing.datamodels.schemas.generated.ca_biositing import (
            DataSource, Dataset, UsdaCensusRecord, UsdaSurveyRecord, Observation
        )

        engine = get_local_engine()
        now = datetime.now(timezone.utc)

        # STEP 0: Create datasets + build map
        logger.info("\nSTEP 0: Creating datasets...")
        dataset_map = _create_and_map_datasets(engine, transformed_df, etl_run_id, lineage_group_id, now)

        # STEP 1: Load census records
        logger.info("\nSTEP 1: Loading census records...")
        census_inserted = _load_census_records(
            engine, transformed_df, dataset_map, etl_run_id,
            lineage_group_id, now
        )

        # STEP 2: Load survey records
        logger.info("\nSTEP 2: Loading survey records...")
        survey_inserted = _load_survey_records(
            engine, transformed_df, dataset_map, etl_run_id,
            lineage_group_id, now
        )

        # STEP 3: Load observations
        logger.info("\nSTEP 3: Loading observations...")
        obs_inserted = _load_observations(
            engine, transformed_df, dataset_map, etl_run_id,
            lineage_group_id, now
        )

        logger.info(f"\nLoad complete:")
        logger.info(f"  Census: {census_inserted}")
        logger.info(f"  Survey: {survey_inserted}")
        logger.info(f"  Observations: {obs_inserted}")

        return True

    except Exception as e:
        logger.error(f"Load failed: {e}", exc_info=True)
        return False


def _create_and_map_datasets(engine, transformed_df, etl_run_id,
                              lineage_group_id, now):
    """STEP 0: Create USDA datasets if needed, return mapping"""
    logger = get_run_logger()
    from ca_biositing.datamodels.schemas.generated.ca_biositing import (
        DataSource, Dataset
    )

    dataset_map = {}
    years = sorted(transformed_df['year'].unique())

    with engine.begin() as conn:
        # Ensure DataSource exists
        result = conn.execute(
            text("SELECT id FROM data_source WHERE name = 'USDA NASS API'")
        )
        ds_row = result.fetchone()
        if not ds_row:
            conn.execute(
                text("""
                    INSERT INTO data_source (name, description, created_at, updated_at)
                    VALUES ('USDA NASS API', 'USDA NASS QuickStats API', :now, :now)
                """),
                {"now": now}
            )
            result = conn.execute(
                text("SELECT id FROM data_source WHERE name = 'USDA NASS API'")
            )
            ds_row = result.fetchone()

        ds_id = ds_row[0]

        # Create datasets for each year
        for year in years:
            for source in ['CENSUS', 'SURVEY']:
                ds_name = f"USDA_{source}_{year}"
                result = conn.execute(
                    text(f"SELECT id FROM dataset WHERE name = '{ds_name}'")
                )
                row = result.fetchone()

                if not row:
                    conn.execute(
                        text("""
                            INSERT INTO dataset
                            (name, record_type, source_id, etl_run_id, lineage_group_id, start_date, end_date,
                             created_at, updated_at)
                            VALUES (:name, :rtype, :sid, :etl_run_id, :lineage_group_id, :start, :end, :now, :now)
                        """),
                        {
                            "name": ds_name,
                            "rtype": f"usda_{source.lower()}_record",
                            "sid": ds_id,
                            "etl_run_id": etl_run_id,
                            "lineage_group_id": lineage_group_id,
                            "start": f"{year}-01-01",
                            "end": f"{year}-12-31",
                            "now": now
                        }
                    )
                    result = conn.execute(
                        text(f"SELECT id FROM dataset WHERE name = '{ds_name}'")
                    )
                    row = result.fetchone()

                dataset_map[(year, source)] = row[0]
                logger.info(f"  Dataset: {ds_name} (id={row[0]})")

    return dataset_map


def _load_census_records(engine, transformed_df, dataset_map, etl_run_id,
                        lineage_group_id, now):
    """STEP 1: Load census records with dedup"""
    logger = get_run_logger()
    from ca_biositing.datamodels.schemas.generated.ca_biositing import UsdaCensusRecord

    # Level 1: Query existing
    existing_keys = set()
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT geoid, year, commodity_code FROM usda_census_record")
        )
        for row in result:
            existing_keys.add((row[0], row[1], row[2]))

    # Build new records with Level 2 dedup
    new_records = []
    seen_keys = set()

    for _, row in transformed_df[transformed_df['source_type'] == 'CENSUS'].iterrows():
        key = (str(row['geoid']).zfill(5), int(row['year']),
               int(row['commodity_code']) if pd.notna(row['commodity_code']) else None)

        if key in existing_keys or key in seen_keys:
            continue

        seen_keys.add(key)
        year = int(row['year'])
        ds_id = dataset_map.get((year, 'CENSUS'))

        new_records.append({
            'geoid': key[0],
            'year': key[1],
            'commodity_code': key[2],
            'source_reference': 'USDA NASS QuickStats API',
            'dataset_id': ds_id,
            'etl_run_id': etl_run_id,
            'lineage_group_id': lineage_group_id,
            'created_at': now,
            'updated_at': now
        })

    if new_records:
        with engine.begin() as conn:
            conn.execute(
                insert(UsdaCensusRecord.__table__),
                new_records
            )
        logger.info(f"  Inserted {len(new_records)} census records")

    return len(new_records)


def _load_survey_records(engine, transformed_df, dataset_map, etl_run_id,
                        lineage_group_id, now):
    """STEP 2: Load survey records with dedup (includes survey-specific fields)"""
    logger = get_run_logger()
    from ca_biositing.datamodels.schemas.generated.ca_biositing import UsdaSurveyRecord

    # Level 1: Query existing
    existing_keys = set()
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT geoid, year, commodity_code FROM usda_survey_record")
        )
        for row in result:
            existing_keys.add((row[0], row[1], row[2]))

    # Build new records with Level 2 dedup
    new_records = []
    seen_keys = set()

    for _, row in transformed_df[transformed_df['source_type'] == 'SURVEY'].iterrows():
        key = (str(row['geoid']).zfill(5), int(row['year']),
               int(row['commodity_code']) if pd.notna(row['commodity_code']) else None)

        if key in existing_keys or key in seen_keys:
            continue

        if not key[2]:  # Skip if no commodity code
            continue

        seen_keys.add(key)
        year = int(row['year'])
        ds_id = dataset_map.get((year, 'SURVEY'))

        new_records.append({
            'geoid': key[0],
            'year': key[1],
            'commodity_code': key[2],
            'source_reference': 'USDA NASS QuickStats API',
            'survey_period': row.get('survey_period') if pd.notna(row.get('survey_period')) else None,
            'reference_month': row.get('reference_month') if pd.notna(row.get('reference_month')) else None,
            'begin_code': row.get('begin_code') if pd.notna(row.get('begin_code')) else None,
            'end_code': row.get('end_code') if pd.notna(row.get('end_code')) else None,
            'dataset_id': ds_id,
            'etl_run_id': etl_run_id,
            'lineage_group_id': lineage_group_id,
            'created_at': now,
            'updated_at': now
        })

    if new_records:
        with engine.begin() as conn:
            conn.execute(
                insert(UsdaSurveyRecord.__table__),
                new_records
            )
        logger.info(f"  Inserted {len(new_records)} survey records")

    return len(new_records)


def _load_observations(engine, transformed_df, dataset_map, etl_run_id,
                      lineage_group_id, now):
    """STEP 3: Load observations with 3-level dedup"""
    logger = get_run_logger()
    from ca_biositing.datamodels.schemas.generated.ca_biositing import Observation

    # Build parent record map
    record_id_map = {}
    with engine.connect() as conn:
        # Census records
        result = conn.execute(
            text("""
                SELECT id, geoid, year, commodity_code
                FROM usda_census_record
            """)
        )
        for record_id, geoid, year, commodity_code in result:
            record_id_map[(geoid, year, commodity_code, 'CENSUS')] = record_id

        # Survey records
        result = conn.execute(
            text("""
                SELECT id, geoid, year, commodity_code
                FROM usda_survey_record
            """)
        )
        for record_id, geoid, year, commodity_code in result:
            record_id_map[(geoid, year, commodity_code, 'SURVEY')] = record_id

    # Level 1: Query existing observations
    existing_obs_keys = set()
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT record_id, record_type, parameter_id, unit_id
                FROM observation
            """)
        )
        for row in result:
            existing_obs_keys.add((row[0], row[1], row[2], row[3]))

    # Build obs records with Level 2 dedup
    obs_records = []
    seen_obs_keys = set()
    table_columns = {c.name for c in Observation.__table__.columns}

    for _, row in transformed_df.iterrows():
        geoid = str(row['geoid']).zfill(5)
        year = int(row['year'])
        commodity_code = int(row['commodity_code']) if pd.notna(row['commodity_code']) else None
        parameter_id = int(row['parameter_id']) if pd.notna(row['parameter_id']) else None
        unit_id = int(row['unit_id']) if pd.notna(row['unit_id']) else None
        value_numeric = float(row['value_numeric']) if pd.notna(row['value_numeric']) else None

        if not all([commodity_code, parameter_id, unit_id, value_numeric]):
            # 🔍 DIAGNOSTIC: Log why records are being filtered
            missing_fields = []
            if commodity_code is None: missing_fields.append("commodity_code")
            if parameter_id is None: missing_fields.append("parameter_id")
            if unit_id is None: missing_fields.append("unit_id")
            if value_numeric is None: missing_fields.append("value_numeric")

            if len(obs_records) < 5:  # Only log first few for brevity
                logger.info(f"❌ Skipping record due to missing: {missing_fields}")
                logger.info(f"   Row values: commodity='{row.get('commodity', 'N/A')}', statistic='{row.get('statistic', 'N/A')}', unit='{row.get('unit', 'N/A')}', value='{row.get('value_numeric', 'N/A')}'")
            continue

        source_type = 'CENSUS' if row['source_type'] == 'CENSUS' else 'SURVEY'
        record_key = (geoid, year, commodity_code, source_type)
        parent_record_id = record_id_map.get(record_key)

        if not parent_record_id:
            continue

        obs_key = (parent_record_id, row['record_type'], parameter_id, unit_id)
        if obs_key in existing_obs_keys or obs_key in seen_obs_keys:
            continue

        seen_obs_keys.add(obs_key)

        # Build observation record with optional fields
        obs_record = {
            'record_id': parent_record_id,
            'record_type': row['record_type'],
            'parameter_id': parameter_id,
            'unit_id': unit_id,
            'value': value_numeric,
            'dataset_id': dataset_map.get((year, source_type)),
            'etl_run_id': etl_run_id,
            'lineage_group_id': lineage_group_id,
            'created_at': now,
            'updated_at': now
        }

        # Add optional fields if present in transformed data and table schema
        if 'value_text' in row and pd.notna(row['value_text']) and 'value_text' in table_columns:
            obs_record['value_text'] = str(row['value_text'])
        if 'cv_pct' in row and pd.notna(row['cv_pct']) and 'cv_pct' in table_columns:
            obs_record['cv_pct'] = float(row['cv_pct'])
        if 'note' in row and pd.notna(row['note']) and 'note' in table_columns:
            obs_record['note'] = str(row['note'])

        # Drop any fields not in the observation table
        obs_record = {k: v for k, v in obs_record.items() if k in table_columns}

        obs_records.append(obs_record)

    # Level 3: PostgreSQL ON CONFLICT
    if obs_records:
        with engine.begin() as conn:
            stmt = pg_insert(Observation.__table__).values(obs_records).on_conflict_do_nothing(
                index_elements=['record_id', 'record_type', 'parameter_id', 'unit_id']
            )
            result = conn.execute(stmt)
            logger.info(f"  Inserted {result.rowcount} observations")
            return result.rowcount

    return 0
