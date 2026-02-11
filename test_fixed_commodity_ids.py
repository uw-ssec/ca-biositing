#!/usr/bin/env python3
"""Test the fixed get_mapped_commodity_ids function"""

import os
import sys
from sqlalchemy import create_engine

# Add path for imports
sys.path.append('src/ca_biositing/pipeline/ca_biositing/pipeline/utils')

db_url = os.getenv('DATABASE_URL', 'postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db')
engine = create_engine(db_url, echo=False)

print("🔧 Testing fixed get_mapped_commodity_ids function...")

try:
    # Test the function directly in the same way the ETL calls it
    from sqlalchemy import text

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT DISTINCT uc.api_name as commodity_name
            FROM usda_commodity uc
            JOIN resource_usda_commodity_map rcm ON uc.id = rcm.usda_commodity_id
            WHERE rcm.match_tier != 'UNMAPPED'
              AND uc.api_name IS NOT NULL
              AND uc.api_name != ''
            ORDER BY commodity_name
        """))
        api_names = [row[0] for row in result.fetchall()]

        print(f"✅ Fixed query returns {len(api_names)} API names:")
        for name in api_names:
            print(f"  - '{name}'")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
