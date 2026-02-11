#!/usr/bin/env python3
import os
from sqlalchemy import create_engine, text

db_url = os.getenv('DATABASE_URL', 'postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db')
engine = create_engine(db_url, echo=False)

with engine.connect() as conn:
    print("🔍 Checking what commodities are in usda_census_record...")
    result = conn.execute(text("""
        SELECT DISTINCT commodity_code, COUNT(*) as record_count
        FROM usda_census_record
        GROUP BY commodity_code
        ORDER BY commodity_code
    """))

    rows = result.fetchall()
    print(f"Found {len(rows)} unique commodities in usda_census_record:")
    for row in rows:
        print(f"  Code: {row[0]}, Records: {row[1]}")

    print("\n📊 Checking what API names we're sending to USDA API...")
    result = conn.execute(text("""
        SELECT DISTINCT uc.api_name, uc.name, uc.usda_code
        FROM usda_commodity uc
        JOIN resource_usda_commodity_map rcm ON uc.id = rcm.usda_commodity_id
        WHERE rcm.match_tier != 'UNMAPPED'
        ORDER BY uc.api_name
    """))

    rows = result.fetchall()
    print(f"Found {len(rows)} mapped API names being sent:")
    for row in rows:
        print(f"  API Name: '{row[0]}', DB Name: '{row[1]}', USDA Code: {row[2]}")
    print("\n🔧 Testing get_mapped_commodity_ids function...")
    try:
        # Add path to find the function
        import sys
        sys.path.append('src/ca_biositing/pipeline/ca_biositing/pipeline/utils')
        from fetch_mapped_commodities import get_mapped_commodity_ids

        api_names = get_mapped_commodity_ids(engine=engine)
        print(f"get_mapped_commodity_ids() returns ({len(api_names) if api_names else 0} items): {api_names}")
    except Exception as e:
        print(f"Error testing get_mapped_commodity_ids: {e}")

    print("\n🔧 Testing get_mapped_commodity_ids function...")
    # Add path to find the function
    import sys
    sys.path.append('src/ca_biositing/pipeline/ca_biositing/pipeline/utils')
    from fetch_mapped_commodities import get_mapped_commodity_ids

    api_names = get_mapped_commodity_ids(engine=engine)
    print(f"get_mapped_commodity_ids() returns: {api_names}")
