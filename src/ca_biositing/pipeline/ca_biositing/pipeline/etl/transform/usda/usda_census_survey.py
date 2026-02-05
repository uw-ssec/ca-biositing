# File: src/ca_biositing/pipeline/etl/transform/usda/usda_census_survey.py
"""
USDA Census/Survey Data Transform
---
Transforms raw USDA API data into normalized records ready for loading.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional
from prefect import task, get_run_logger
from sqlalchemy import create_engine


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
def transform(
    data_sources: Dict[str, pd.DataFrame],
    etl_run_id: int,
    lineage_group_id: int
) -> Optional[pd.DataFrame]:
    """
    Transform raw USDA data into database-ready format.

    Args:
        data_sources: {"usda": raw_dataframe}
        etl_run_id: For tracking this ETL run
        lineage_group_id: For grouping related records

    Returns:
        Transformed DataFrame ready for load task
    """
    logger = get_run_logger()
    logger.info("🟡 [USDA Transform] Starting...")

    if "usda" not in data_sources:
        logger.error("Missing 'usda' in data_sources")
        return None

    logger.info(f"🟡 [USDA Transform] Received {len(data_sources['usda'])} raw records")

    raw_data = data_sources["usda"]

    if raw_data is None or len(raw_data) == 0:
        logger.warning("No raw data to transform")
        return None

    logger.info(f"🟡 [USDA Transform] Transforming {len(raw_data)} raw records...")

    # --- LAZY IMPORT (critical for Docker) ---
    # Import models inside task to avoid module-level hangs
    logger.info("🟡 [USDA Transform] Step 0a: Importing database modules...")
    try:
        from sqlmodel import Session, select
        logger.info("🟡 [USDA Transform] Step 0a.1: SQLModel imported")
    except Exception as e:
        logger.error(f"Failed to import SQLModel: {e}")
        raise

    try:
        from ca_biositing.datamodels.schemas.generated.ca_biositing import (
            Parameter, Unit
        )
        logger.info("🟡 [USDA Transform] Step 0a.2: Models imported")
    except Exception as e:
        logger.error(f"Failed to import models: {e}")
        raise

    # 1. Ensure Parameter/Unit records exist
    logger.info("🟡 [USDA Transform] Step 0b: Creating Parameter/Unit records if needed...")
    try:
        engine = get_local_engine()
        logger.info("🟡 [USDA Transform] Step 0b.1: Engine created")
        _ensure_parameters_and_units(engine)
        logger.info("🟡 [USDA Transform] Step 0b.2: Parameters/Units ready")
    except Exception as e:
        logger.error(f"Failed in Step 0b: {e}")
        raise

    # 1. Ensure Parameter/Unit records exist
    logger.info("🟡 [USDA Transform] Step 0b: Creating Parameter/Unit records if needed...")
    _ensure_parameters_and_units(engine)
    logger.info("🟡 [USDA Transform] Step 0b: Parameters/Units ready")

    # Build lookup maps (build once, use for all 6908 rows)
    logger.info("🟡 [USDA Transform] Step 0c: Building lookup maps from database...")
    commodity_map, parameter_id_map, unit_id_map = _build_lookup_maps()
    logger.info(f"  ✓ Commodity map: {len(commodity_map)} entries")
    logger.info(f"  ✓ Parameter map: {len(parameter_id_map)} entries")
    logger.info(f"  ✓ Unit map: {len(unit_id_map)} entries")

    # 2. Construct geoid
    logger.info("🟡 [USDA Transform] Step 1: Constructing geoid...")
    transformed_data = _normalize_geoid(raw_data)
    logger.info("  ✓ Geoid constructed")

    # 3. Rename columns
    logger.info("🟡 [USDA Transform] Step 2: Normalizing columns...")
    transformed_data = _normalize_columns(transformed_data)
    logger.info("  ✓ Columns normalized")

    # 4. Set source_type (CENSUS vs SURVEY)
    logger.info("🟡 [USDA Transform] Step 3: Setting source_type...")
    if 'source_type' not in transformed_data.columns and 'source_desc' in transformed_data.columns:
        transformed_data['source_type'] = transformed_data['source_desc'].map(
            {'CENSUS': 'CENSUS', 'SURVEY': 'SURVEY'},
            na_action='ignore'
        )
    transformed_data['source_type'] = transformed_data['source_type'].fillna('CENSUS')
    logger.info("  ✓ Source type set")

    # 5. Clean strings
    logger.info("🟡 [USDA Transform] Step 4: Cleaning string fields...")
    transformed_data = _clean_strings(transformed_data)
    logger.info("  ✓ Strings cleaned")

    # 6. Convert values to numeric
    logger.info("🟡 [USDA Transform] Step 5: Converting values to numeric...")
    transformed_data['value_numeric'] = _convert_to_numeric(
        transformed_data['observation']
    )
    # Also store original value as text
    if 'observation' in transformed_data.columns:
        transformed_data['value_text'] = transformed_data['observation'].astype(str)
    logger.info("  ✓ Values converted")

    # 7. Map IDs (vectorized - much faster than apply())
    logger.info("🟡 [USDA Transform] Step 6: Mapping IDs...")
    # Uppercase the columns before mapping for case-insensitive lookup
    logger.info("  → Mapping commodities...")
    transformed_data['commodity_code'] = transformed_data['commodity'].fillna('').str.upper().map(commodity_map)
    logger.info("  → Mapping parameters...")
    transformed_data['parameter_id'] = transformed_data['statistic'].fillna('').str.upper().map(parameter_id_map)
    logger.info("  → Mapping units...")
    transformed_data['unit_id'] = transformed_data['unit'].fillna('').str.upper().map(unit_id_map)
    logger.info("  ✓ All IDs mapped")

    # 8. Add record type discriminator
    logger.info("🟡 [USDA Transform] Step 7: Adding record type...")
    transformed_data['record_type'] = transformed_data['source_type'].map({
        'CENSUS': 'usda_census_record',
        'SURVEY': 'usda_survey_record'
    })
    logger.info("  ✓ Record type added")

    # 9. Handle coefficient of variation (CV%) if present
    logger.info("🟡 [USDA Transform] Step 8: Processing optional fields...")
    if 'CV (%)' in transformed_data.columns:
        transformed_data['cv_pct'] = pd.to_numeric(transformed_data['CV (%)'], errors='coerce')
    logger.info("  ✓ Optional fields processed")

    # 10. Coerce ID columns to proper integer types
    logger.info("🟡 [USDA Transform] Step 9: Coercing ID columns...")
    id_columns = ['commodity_code', 'parameter_id', 'unit_id']
    for col in id_columns:
        if col in transformed_data.columns:
            transformed_data[col] = pd.to_numeric(transformed_data[col], errors='coerce').astype('Int64')
    logger.info("  ✓ ID columns coerced")

    # 11. Create note field from components (vectorized)
    logger.info("🟡 [USDA Transform] Step 10: Creating note field...")
    transformed_data['note'] = (
        transformed_data.get('statistic', 'N/A').fillna('N/A').astype(str) + ' in ' +
        transformed_data.get('unit', 'N/A').fillna('N/A').astype(str) + ' for ' +
        transformed_data.get('commodity', 'N/A').fillna('N/A').astype(str) + ' in ' +
        transformed_data.get('county', 'N/A').fillna('N/A').astype(str)
    )
    logger.info("  ✓ Note field created")

    # 12. Add metadata
    logger.info("🟡 [USDA Transform] Step 11: Adding metadata...")
    transformed_data['etl_run_id'] = etl_run_id
    transformed_data['lineage_group_id'] = lineage_group_id
    logger.info("  ✓ Metadata added")

    # 13. Filter required fields
    logger.info("🟡 [USDA Transform] Step 12: Filtering required fields...")
    required = ['geoid', 'year', 'commodity_code', 'parameter_id', 'unit_id', 'value_numeric']
    transformed_data = transformed_data.dropna(subset=required)
    logger.info("  ✓ Required fields filtered")

    logger.info(f"🟢 [USDA Transform] Complete: {len(transformed_data)} records ready for load")
    return transformed_data


def _build_lookup_maps():
    """Build commodity, parameter, unit maps from database"""
    from sqlalchemy import text

    engine = get_local_engine()

    commodity_map = {}
    parameter_map = {}
    unit_map = {}

    with engine.connect() as conn:
        # Commodities
        result = conn.execute(text("SELECT id, name FROM usda_commodity"))
        for row in result:
            commodity_map[row[1].upper()] = row[0]

        # Parameters
        result = conn.execute(text("SELECT id, name FROM parameter"))
        for row in result:
            parameter_map[row[1].upper()] = row[0]

        # Units
        result = conn.execute(text("SELECT id, name FROM unit"))
        for row in result:
            unit_map[row[1].upper()] = row[0]

    return commodity_map, parameter_map, unit_map


def _normalize_geoid(df):
    """Construct 5-digit FIPS geoid from state + county codes"""
    df = df.copy()
    state_fips_default = '06'  # California

    if 'state_fips_code' in df.columns and 'county_code' in df.columns:
        df['geoid'] = df['state_fips_code'].astype(str).str.zfill(2) + \
                      df['county_code'].astype(str).str.zfill(3)
    elif 'county_code' in df.columns:
        df['geoid'] = state_fips_default + df['county_code'].astype(str).str.zfill(3)
    else:
        df['geoid'] = None

    df['geoid'] = df['geoid'].astype(str).str.zfill(5)
    return df


def _normalize_columns(df):
    """Rename USDA columns to match schema"""
    mapping = {
        'commodity_desc': 'commodity',
        'statisticcat_desc': 'statistic',
        'unit_desc': 'unit',
        'Value': 'observation',
        'county_name': 'county',
        'year': 'year',
        'freq_desc': 'survey_period',
        'reference_period_desc': 'reference_month',
        'begin_code': 'begin_code',
        'end_code': 'end_code',
        'source_desc': 'source_type'
    }
    return df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})


def _clean_strings(df):
    """Clean string columns: replace empty/whitespace with NaN, then lowercase"""
    df = df.copy()

    # Replace empty/whitespace-only strings with NaN
    str_cols = ['commodity', 'statistic', 'unit', 'county', 'survey_period', 'reference_month']
    str_cols = [c for c in str_cols if c in df.columns]

    for col in str_cols:
        df[col] = df[col].replace(r'^\s*$', np.nan, regex=True)
        # Lowercase for consistency
        df[col] = df[col].astype('string').str.lower().where(df[col].notna(), df[col])

    return df


def _convert_to_numeric(series):
    """Convert to numeric, handling commas and decimals"""
    return pd.to_numeric(
        series.astype(str).str.replace(',', ''),
        errors='coerce'
    )


def _ensure_parameters_and_units(engine):
    """Create Parameter/Unit records if they don't exist (idempotent)"""
    from sqlmodel import Session, select
    from ca_biositing.datamodels.schemas.generated.ca_biositing import Parameter, Unit

    PARAMETER_CONFIGS = {
        'YIELD': 'Yield per unit area',
        'PRODUCTION': 'Total production quantity',
        'AREA HARVESTED': 'Area harvested',
        'AREA PLANTED': 'Area planted',
        'PRICE RECEIVED': 'Price received by farmer',
        'PRICE PAID': 'Price paid by farmer',
    }

    UNIT_CONFIGS = {
        'BUSHELS': 'US bushels',
        'TONS': 'Short tons (US)',
        'ACRES': 'US acres',
        'DOLLARS': 'US dollars',
        'DOLLARS PER BUSHEL': 'US dollars per bushel',
        'DOLLARS PER TON': 'US dollars per ton',
    }

    with Session(engine) as session:
        # Get existing parameters
        existing_params = session.exec(select(Parameter.name)).all()
        existing_param_names = set(existing_params)

        # Add only new parameters (lowercase names for consistency)
        params_to_add = []
        for param_name, param_desc in PARAMETER_CONFIGS.items():
            param_name_lower = param_name.lower()
            if param_name_lower not in existing_param_names:
                param = Parameter(name=param_name_lower, description=param_desc, calculated=False)
                params_to_add.append(param)
                existing_param_names.add(param_name_lower)

        if params_to_add:
            session.add_all(params_to_add)

        # Get existing units
        existing_units = session.exec(select(Unit.name)).all()
        existing_unit_names = set(existing_units)

        # Add only new units (lowercase names for consistency)
        units_to_add = []
        for unit_name, unit_desc in UNIT_CONFIGS.items():
            unit_name_lower = unit_name.lower()
            if unit_name_lower not in existing_unit_names:
                unit = Unit(name=unit_name_lower, description=unit_desc)
                units_to_add.append(unit)
                existing_unit_names.add(unit_name_lower)

        if units_to_add:
            session.add_all(units_to_add)

        # Commit only if we added anything
        if params_to_add or units_to_add:
            session.commit()
