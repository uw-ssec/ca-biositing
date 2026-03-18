# File: src/ca_biositing/pipeline/etl/transform/usda/usda_census_survey.py
"""
USDA Census/Survey Data Transform.

Transforms raw USDA API data into normalized records ready for loading.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional
from prefect import task, get_run_logger
from ca_biositing.pipeline.utils.engine import get_engine


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
    logger.info("[USDA Transform] Starting transform step...")

    if "usda" not in data_sources:
        logger.error("Missing 'usda' in data_sources")
        return None

    raw_data = data_sources['usda']
    logger.info(f"[USDA Transform] Processing {len(raw_data)} raw records")

    # 🔍 DIAGNOSTIC: Log raw data info
    logger.info(f"Raw data shape: {raw_data.shape}")
    if 'commodity_desc' in raw_data.columns:
        commodities = raw_data['commodity_desc'].unique()
        logger.info(f"Raw commodities: {len(commodities)} unique")

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
        from ca_biositing.datamodels.models import (
            Parameter, Unit
        )
        logger.info("🟡 [USDA Transform] Step 0a.2: Models imported")
    except Exception as e:
        logger.error(f"Failed to import models: {e}")
        raise

    # 1. Ensure Parameter/Unit records exist
    logger.info("🟡 [USDA Transform] Step 0b: Creating Parameter/Unit records if needed...")
    try:
        engine = get_engine()
        logger.info("🟡 [USDA Transform] Step 0b.1: Engine created")
        _ensure_parameters_and_units(engine)
        logger.info("🟡 [USDA Transform] Step 0b.2: Parameters/Units ready")
    except Exception as e:
        logger.error(f"Failed in Step 0b: {e}")
        raise

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

    # 🔍 DIAGNOSTIC: Analyze non-numeric values before conversion
    logger.info("📊 DIAGNOSTIC: Analyzing observation values before numeric conversion...")
    if 'observation' in transformed_data.columns:
        # Show unique observation values and their counts
        obs_counts = transformed_data['observation'].value_counts()
        logger.info(f"📊 Found {len(obs_counts)} unique observation values:")

        # Show most common values (especially non-numeric ones)
        for value, count in obs_counts.head(20).items():
            logger.info(f"  '{value}': {count} occurrences")

        # Specifically look for USDA special codes
        special_codes = ['(D)', '(Z)', '(NA)', '', 'null', 'NULL', 'nan', 'NaN']
        for code in special_codes:
            code_count = (transformed_data['observation'] == code).sum()
            if code_count > 0:
                logger.warning(f"⚠️  Found {code_count} rows with USDA special code: '{code}'")

    transformed_data['value_numeric'] = _convert_to_numeric(
        transformed_data['observation']
    )

    # 🔍 DIAGNOSTIC: Report conversion results
    total_rows = len(transformed_data)
    null_values = transformed_data['value_numeric'].isna().sum()
    numeric_values = total_rows - null_values
    logger.info(f"📊 Numeric conversion results:")
    logger.info(f"  ✅ Successfully converted: {numeric_values}/{total_rows} ({100*numeric_values/total_rows:.1f}%)")
    if null_values > 0:
        logger.warning(f"  ❌ Failed conversion (now null): {null_values}/{total_rows} ({100*null_values/total_rows:.1f}%)")

    # Also store original value as text
    if 'observation' in transformed_data.columns:
        transformed_data['value_text'] = transformed_data['observation'].astype(str)
    logger.info("  ✓ Values converted")

    # 7. Map IDs (vectorized - much faster than apply())
    logger.info("🟡 [USDA Transform] Step 6: Mapping IDs...")
    # Uppercase the columns before mapping for case-insensitive lookup
    logger.info("  → Mapping commodities...")

    # 🔍 DETAILED DIAGNOSTIC: Show complete commodity mapping analysis
    logger.info("📋 COMPLETE commodity mapping analysis:")
    logger.info(f"📊 Available commodity mapping keys ({len(commodity_map)} total):")
    for key, value in commodity_map.items():
        logger.info(f"  DB: '{key}' → ID {value}")

    unique_commodities = transformed_data['commodity'].fillna('').unique()
    logger.info(f"📊 Unique commodity values in raw data ({len(unique_commodities)} total):")
    for commodity in unique_commodities:
        upper_commodity = str(commodity).upper()
        mapped_value = commodity_map.get(upper_commodity, 'NOT_FOUND')
        count = len(transformed_data[transformed_data['commodity'] == commodity])
        status = "✅" if mapped_value != 'NOT_FOUND' else "❌"
        logger.info(f"  {status} '{commodity}' → '{upper_commodity}' → {mapped_value} ({count} rows)")

    # 🔍 FRUIT/NUT SPECIFIC ANALYSIS
    fruit_nuts = ['almonds', 'grapes', 'olives', 'peaches', 'pistachios', 'walnuts']
    logger.info("🍎 FRUIT/NUT commodity analysis:")
    for fruit in fruit_nuts:
        fruit_rows = transformed_data[transformed_data['commodity'].str.lower() == fruit]
        if len(fruit_rows) > 0:
            logger.info(f"  🔍 Found {len(fruit_rows)} rows for '{fruit}'")
            sample_statistic = fruit_rows['statistic'].iloc[0] if len(fruit_rows) > 0 else 'N/A'
            sample_unit = fruit_rows['unit'].iloc[0] if len(fruit_rows) > 0 else 'N/A'
            logger.info(f"     Sample statistic: '{sample_statistic}'")
            logger.info(f"     Sample unit: '{sample_unit}'")
        else:
            logger.info(f"  ❌ No rows found for '{fruit}'")

    # Perform the actual mapping
    transformed_data['commodity_code'] = transformed_data['commodity'].fillna('').str.upper().map(commodity_map)

    # 🔍 MAPPING RESULTS BY COMMODITY
    commodity_mapping_summary = transformed_data.groupby(['commodity', 'commodity_code']).size().reset_index(name='count')
    logger.info("📊 DETAILED mapping results by commodity:")
    for _, row in commodity_mapping_summary.iterrows():
        status = "✅ MAPPED" if pd.notna(row['commodity_code']) else "❌ UNMAPPED"
        logger.info(f"  {status} '{row['commodity']}' → ID {row['commodity_code']} ({row['count']} rows)")

    successful_mappings = transformed_data['commodity_code'].notna().sum()
    total_rows = len(transformed_data)
    logger.info(f"📈 SUMMARY: {successful_mappings}/{total_rows} rows successfully mapped commodity codes")

    # 🔍 DETAILED UNMAPPED ANALYSIS
    unmapped = transformed_data[transformed_data['commodity_code'].isna()]
    if len(unmapped) > 0:
        logger.warning(f"⚠️  {len(unmapped)} rows failed commodity mapping!")
        unmapped_commodities = unmapped['commodity'].value_counts()
        logger.warning("❌ Unmapped commodities breakdown:")
        for commodity, count in unmapped_commodities.items():
            logger.warning(f"   '{commodity}': {count} rows")
            # Show sample statistics and units for unmapped commodities
            sample_data = unmapped[unmapped['commodity'] == commodity].iloc[0]
            logger.warning(f"      Sample statistic: '{sample_data.get('statistic', 'N/A')}'")
            logger.warning(f"      Sample unit: '{sample_data.get('unit', 'N/A')}'")

    logger.info("  → Mapping parameters...")

    # 🔍 PARAMETER MAPPING DIAGNOSTICS
    logger.info("📋 Available parameter mapping keys:")
    for key, value in parameter_id_map.items():
        logger.info(f"  PARAM: '{key}' → ID {value}")

    unique_statistics = transformed_data['statistic'].fillna('').unique()
    logger.info(f"📊 Unique statistics in data ({len(unique_statistics)} total):")
    for statistic in unique_statistics:
        upper_stat = str(statistic).upper()
        mapped_value = parameter_id_map.get(upper_stat, 'NOT_FOUND')
        count = len(transformed_data[transformed_data['statistic'] == statistic])
        status = "✅" if mapped_value != 'NOT_FOUND' else "❌"
        logger.info(f"  {status} '{statistic}' → '{upper_stat}' → {mapped_value} ({count} rows)")

    transformed_data['parameter_id'] = transformed_data['statistic'].fillna('').str.upper().map(parameter_id_map)

    # 🔍 PARAMETER MAPPING RESULTS
    param_mapping_summary = transformed_data.groupby(['statistic', 'parameter_id']).size().reset_index(name='count')
    logger.info("📊 Parameter mapping results:")
    for _, row in param_mapping_summary.iterrows():
        status = "✅ MAPPED" if pd.notna(row['parameter_id']) else "❌ UNMAPPED"
        logger.info(f"  {status} '{row['statistic']}' → ID {row['parameter_id']} ({row['count']} rows)")

    logger.info("  → Mapping units...")

    # 🔍 UNIT MAPPING DIAGNOSTICS
    logger.info("📋 Available unit mapping keys:")
    for key, value in unit_id_map.items():
        logger.info(f"  UNIT: '{key}' → ID {value}")

    unique_units = transformed_data['unit'].fillna('').unique()
    logger.info(f"📊 Unique units in data ({len(unique_units)} total):")
    for unit in unique_units:
        upper_unit = str(unit).upper()
        mapped_value = unit_id_map.get(upper_unit, 'NOT_FOUND')
        count = len(transformed_data[transformed_data['unit'] == unit])
        status = "✅" if mapped_value != 'NOT_FOUND' else "❌"
        logger.info(f"  {status} '{unit}' → '{upper_unit}' → {mapped_value} ({count} rows)")

    transformed_data['unit_id'] = transformed_data['unit'].fillna('').str.upper().map(unit_id_map)

    # 🔍 UNIT MAPPING RESULTS
    unit_mapping_summary = transformed_data.groupby(['unit', 'unit_id']).size().reset_index(name='count')
    logger.info("📊 Unit mapping results:")
    for _, row in unit_mapping_summary.iterrows():
        status = "✅ MAPPED" if pd.notna(row['unit_id']) else "❌ UNMAPPED"
        logger.info(f"  {status} '{row['unit']}' → ID {row['unit_id']} ({row['count']} rows)")

    logger.info("  ✓ All ID mappings attempted")

    # 🔍 COMBINED MAPPING SUCCESS ANALYSIS
    successful_commodity = transformed_data['commodity_code'].notna().sum()
    successful_parameter = transformed_data['parameter_id'].notna().sum()
    successful_unit = transformed_data['unit_id'].notna().sum()
    total_rows = len(transformed_data)

    logger.info(f"📈 MAPPING SUCCESS RATES:")
    logger.info(f"   Commodities: {successful_commodity}/{total_rows} ({100*successful_commodity/total_rows:.1f}%)")
    logger.info(f"   Parameters:  {successful_parameter}/{total_rows} ({100*successful_parameter/total_rows:.1f}%)")
    logger.info(f"   Units:       {successful_unit}/{total_rows} ({100*successful_unit/total_rows:.1f}%)")

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

    # 🔍 DETAILED ANALYSIS BEFORE FILTERING
    rows_before = len(transformed_data)
    logger.info(f"📊 BEFORE filtering: {rows_before} rows")

    # Check each required field for null values
    for field in required:
        null_count = transformed_data[field].isna().sum()
        if null_count > 0:
            logger.warning(f"⚠️  Field '{field}' has {null_count} null values")
            # Show which commodities have null values for this field
            null_data = transformed_data[transformed_data[field].isna()]
            commodity_nulls = null_data.groupby('commodity').size().reset_index(name='count')
            logger.warning(f"   Commodities with null '{field}':")
            for _, row in commodity_nulls.iterrows():
                logger.warning(f"     '{row['commodity']}': {row['count']} rows")
        else:
            logger.info(f"✅ Field '{field}' has no null values")

    # 🔍 FRUIT/NUT ANALYSIS BEFORE FILTERING
    fruit_nuts = ['almonds', 'grapes', 'olives', 'peaches', 'pistachios', 'walnuts']
    logger.info("🍎 FRUIT/NUT analysis before filtering:")
    for fruit in fruit_nuts:
        fruit_rows = transformed_data[transformed_data['commodity'].str.lower() == fruit]
        if len(fruit_rows) > 0:
            logger.info(f"  🔍 '{fruit}': {len(fruit_rows)} rows")
            for field in required:
                null_count = fruit_rows[field].isna().sum()
                if null_count > 0:
                    logger.warning(f"     ❌ '{field}' has {null_count} nulls")
                else:
                    logger.info(f"     ✅ '{field}' OK")

    # Perform the filtering
    transformed_data = transformed_data.dropna(subset=required)

    # 🔍 DETAILED ANALYSIS AFTER FILTERING
    rows_after = len(transformed_data)
    rows_filtered = rows_before - rows_after
    logger.info(f"📊 AFTER filtering: {rows_after} rows ({rows_filtered} filtered out)")

    if rows_filtered > 0:
        logger.warning(f"⚠️  FILTERED OUT {rows_filtered} rows due to missing required fields")

    # Check which commodities survived filtering
    surviving_commodities = transformed_data['commodity'].value_counts()
    logger.info(f"📊 Surviving commodities after filtering ({len(surviving_commodities)} total):")
    for commodity, count in surviving_commodities.items():
        logger.info(f"  ✅ '{commodity}': {count} rows")

    # 🔍 FRUIT/NUT SURVIVAL ANALYSIS
    logger.info("🍎 FRUIT/NUT survival analysis:")
    for fruit in fruit_nuts:
        fruit_rows_after = transformed_data[transformed_data['commodity'].str.lower() == fruit]
        if len(fruit_rows_after) > 0:
            logger.info(f"  ✅ '{fruit}': {len(fruit_rows_after)} rows survived")
        else:
            logger.warning(f"  ❌ '{fruit}': COMPLETELY FILTERED OUT")

    logger.info("  ✓ Required fields filtering complete")

    # 🔍 DIAGNOSTIC: Save transformed data for inspection (OPTIONAL - uncomment to enable)
    # Uncomment the following block to generate debug CSV files for troubleshooting
    # try:
    #     from datetime import datetime
    #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #     debug_csv_path = f"/app/data/usda_transformed_debug_{timestamp}.csv"
    #     transformed_data.to_csv(debug_csv_path, index=False)
    #     logger.info(f"💾 Debug: Transformed data saved to {debug_csv_path}")

    #     # Show unique commodity codes that made it through
    #     unique_commodities = transformed_data['commodity_code'].value_counts()
    #     logger.info(f"📈 Unique commodity codes in final data: {len(unique_commodities)}")
    #     for commodity_code, count in unique_commodities.head(10).items():
    #         logger.info(f"  Commodity {commodity_code}: {count} records")
    # except Exception as e:
    #     logger.warning(f"Could not save debug CSV: {e}")

    logger.info(f"📊 Final shape: {transformed_data.shape} (rows x columns)")

    logger.info(f"🟢 [USDA Transform] Complete: {len(transformed_data)} records ready for load")
    return transformed_data


def _build_lookup_maps():
    """Build commodity, parameter, unit maps from database"""
    from sqlalchemy import text

    engine = get_engine()

    commodity_map = {}
    parameter_map = {}
    unit_map = {}

    with engine.connect() as conn:
        # Commodities - use api_name instead of name since that's what USDA API returns
        result = conn.execute(text("SELECT id, api_name FROM usda_commodity"))
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
    from ca_biositing.datamodels.models import Parameter, Unit

    PARAMETER_CONFIGS = {
        'YIELD': 'Yield per unit area',
        'PRODUCTION': 'Total production quantity',
        'AREA HARVESTED': 'Area harvested',
        'AREA PLANTED': 'Area planted',
        'AREA BEARING': 'Area with bearing trees/vines (fruit/nut specific)',
        'AREA NON-BEARING': 'Area with non-bearing trees/vines (fruit/nut specific)',
        'AREA BEARING & NON-BEARING': 'Total area with bearing and non-bearing trees/vines',
        'OPERATIONS': 'Number of farming operations/establishments',
        'PRICE RECEIVED': 'Price received by farmer',
        'PRICE PAID': 'Price paid by farmer',
        'SALES': 'Sales value or operations with sales',
        # Additional parameters found in USDA data
        'AREA PLANTED, NET': 'Net area planted',
        'ACTIVE GINS': 'Number of active cotton gins',
        'GINNED BALES': 'Cotton bales ginned',
        'AREA IN PRODUCTION': 'Area in production',
    }

    UNIT_CONFIGS = {
        'BUSHELS': 'US bushels',
        'TONS': 'Short tons (US)',
        'ACRES': 'US acres',
        'DOLLARS': 'US dollars',
        'DOLLARS PER BUSHEL': 'US dollars per bushel',
        'DOLLARS PER TON': 'US dollars per ton',
        'OPERATIONS': 'Number of farming operations/establishments',
        # Additional units found in USDA data
        'BU': 'US bushels (abbreviated)',
        '$': 'US dollars (symbol)',
        'LB': 'Pounds',
        'BU / ACRE': 'Bushels per acre (yield)',
        'BU / NET PLANTED ACRE': 'Bushels per net planted acre',
        'TONS / ACRE': 'Tons per acre (yield)',
        'LB / ACRE': 'Pounds per acre (yield)',
        'LB / NET PLANTED ACRE': 'Pounds per net planted acre',
        'BALES': 'Cotton bales',
        '480 LB BALES': 'Cotton bales (480 lb standard)',
        'RUNNING BALES': 'Running bales (cotton)',
        'LB / BALE, AVG': 'Average pounds per bale',
        'NUMBER': 'Count/number',
        'CWT': 'Hundredweight (100 pounds)',
        'SQ FT': 'Square feet',
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
