#!/usr/bin/env python3
"""
Test script to manually run commodity mapping seeding
"""

import sys
import os

# Add the pipeline utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'ca_biositing', 'pipeline', 'ca_biositing', 'pipeline', 'utils'))

from seed_commodity_mappings import seed_commodity_mappings_from_csv, check_seeding_prerequisites

def main():
    print("🔍 Checking prerequisites...")
    prereqs = check_seeding_prerequisites()
    print(f"Prerequisites: {prereqs}")

    print("\n🌱 Running commodity mapping seeding...")
    success = seed_commodity_mappings_from_csv()

    if success:
        print("✅ Seeding completed successfully!")
    else:
        print("❌ Seeding failed!")

    # Now check what's in the usda_commodity table
    print("\n📊 Checking usda_commodity table...")
    from sqlalchemy import create_engine, text

    db_url = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db"
    )
    engine = create_engine(db_url, echo=False)

    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, name, api_name, usda_code, uri FROM usda_commodity LIMIT 5"))
        rows = result.fetchall()
        print("Sample rows:")
        for row in rows:
            print(f"  ID: {row[0]}, Name: '{row[1]}', API Name: '{row[2]}', USDA Code: {row[3]} ({type(row[3])}), URI: '{row[4]}'")

if __name__ == "__main__":
    main()
