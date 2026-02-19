import pandas as pd
from sqlalchemy import create_engine, text

def get_database_engine():
    """Try to connect to database on different ports."""
    ports = [9090, 5432]  # Try containerized port first, then default

    for port in ports:
        try:
            engine = create_engine(f'postgresql://biocirv_user:biocirv_dev_password@localhost:{port}/biocirv_db')
            # Test the connection
            with engine.connect() as conn:
                conn.execute(text('SELECT 1'))
            print(f"✅ Connected to database on port {port}")
            return engine
        except Exception as e:
            print(f"❌ Failed to connect on port {port}: {e}")
            continue

    raise Exception("Could not connect to database on any port")

engine = get_database_engine()
with engine.connect() as conn:
    print("🔍 COMPREHENSIVE DATABASE COMMODITY ANALYSIS")
    print("=" * 60)

    # Check usda_commodity table
    result = conn.execute(text('SELECT id, name, api_name FROM usda_commodity ORDER BY id'))
    commodities = {row[0]: {'name': row[1], 'api_name': row[2]} for row in result}
    print(f'\n=== USDA_COMMODITY TABLE ({len(commodities)} total) ===')
    for id, info in commodities.items():
        print(f'{id:3}: name="{info["name"]}" api_name="{info["api_name"]}"')

    # Check what data is in census records
    result = conn.execute(text('SELECT DISTINCT commodity_code FROM usda_census_record ORDER BY commodity_code'))
    census_codes = [row[0] for row in result]
    print(f'\n=== COMMODITY CODES IN CENSUS RECORDS ({len(census_codes)} codes) ===')
    for code in census_codes:
        commodity_info = commodities.get(code, {'name': 'UNKNOWN', 'api_name': 'UNKNOWN'})
        print(f'  {code:3}: {commodity_info["api_name"]} ({commodity_info["name"]})')

    # Check what data is in survey records
    result = conn.execute(text('SELECT DISTINCT commodity_code FROM usda_survey_record ORDER BY commodity_code'))
    survey_codes = [row[0] for row in result]
    print(f'\n=== COMMODITY CODES IN SURVEY RECORDS ({len(survey_codes)} codes) ===')
    for code in survey_codes:
        commodity_info = commodities.get(code, {'name': 'UNKNOWN', 'api_name': 'UNKNOWN'})
        print(f'  {code:3}: {commodity_info["api_name"]} ({commodity_info["name"]})')

    # Summary analysis
    print(f'\n=== SUMMARY ANALYSIS ===')
    census_set = set(census_codes)
    survey_set = set(survey_codes)
    all_codes = census_set.union(survey_set)

    print(f'Total unique commodities in database: {len(all_codes)}')
    print(f'Commodities in both census and survey: {len(census_set.intersection(survey_set))}')
    print(f'Census-only commodities: {len(census_set - survey_set)}')
    print(f'Survey-only commodities: {len(survey_set - census_set)}')

    if census_set - survey_set:
        print(f'Census-only: {sorted(census_set - survey_set)}')
    if survey_set - census_set:
        print(f'Survey-only: {sorted(survey_set - census_set)}')

    # Check observation counts
    result = conn.execute(text("""
        SELECT
            record_type,
            COUNT(*) as observation_count,
            COUNT(DISTINCT record_id) as unique_records
        FROM observation
        WHERE record_type IN ('usda_census_record', 'usda_survey_record')
        GROUP BY record_type
    """))

    print(f'\n=== OBSERVATION DATA ===')
    for row in result:
        print(f'{row[0]}: {row[1]} observations from {row[2]} unique records')
