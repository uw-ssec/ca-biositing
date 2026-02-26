"""
USDA Commodity Mapping Seeder
---
This module seeds the usda_commodity and resource_usda_commodity_map tables
using the CSV mapping file. It assumes that the primary_ag_product and resource
tables are already populated by previous flows.

TODO: Eventually expand usda_commodity table to include ALL USDA commodities
and their official API names for complete coverage, not just mapped ones.
This would enable broader agricultural data analysis beyond current resource mappings.
"""

import os
import pandas as pd
from sqlalchemy import text
from ca_biositing.pipeline.utils.engine import get_engine


def seed_commodity_mappings_from_csv(csv_path: str = None, engine=None) -> bool:
    """
    Seed usda_commodity and resource_usda_commodity_map tables from CSV mapping file.

    Args:
        csv_path: Path to CSV mapping file (defaults to pipeline utils directory)
        engine: SQLAlchemy engine (optional, will create if None)

    Returns:
        bool: True if seeding succeeded, False otherwise
    """

    try:
        if engine is None:
            engine = get_engine()

        # Default CSV path (name-based format)
        if csv_path is None:
            current_dir = os.path.dirname(__file__)
            csv_path = os.path.join(current_dir, "commodity_mappings.csv")

        if not os.path.exists(csv_path):
            print(f"❌ Mapping CSV file not found: {csv_path}")
            return False


        # Read CSV mapping file
        print(f"📊 Reading mapping file: {csv_path}")
        df = pd.read_csv(csv_path)

        # Normalize relevant columns to lowercase and strip whitespace
        for col in ["commodity_name", "api_name", "resource_name"]:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.lower()

        # Filter out unmapped entries
        mapped_df = df[df['match_tier'] != 'UNMAPPED'].copy()
        print(f"📊 Found {len(mapped_df)} mapped commodities (excluding {len(df) - len(mapped_df)} unmapped)")

        with engine.connect() as conn:
            # Start transaction
            trans = conn.begin()

            try:
                # 1. Seed usda_commodity table (unique commodities only)
                print("🌱 Seeding usda_commodity table...")
                unique_commodities = mapped_df.drop_duplicates('commodity_name')[
                    ['commodity_name', 'api_name', 'usda_code']
                ].copy()

                for _, row in unique_commodities.iterrows():
                    # First check if commodity already exists
                    existing_result = conn.execute(text(
                        "SELECT id FROM usda_commodity WHERE name = :name"
                    ), {'name': row['commodity_name']})
                    existing_row = existing_result.fetchone()

                    if existing_row:
                        # Update existing record
                        conn.execute(text("""
                            UPDATE usda_commodity
                            SET api_name = :api_name, usda_code = :usda_code, updated_at = NOW()
                            WHERE name = :name
                        """), {
                            'name': row['commodity_name'],
                            'api_name': row['api_name'],
                            'usda_code': int(row['usda_code'])
                        })
                    else:
                        # Insert new record
                        conn.execute(text("""
                            INSERT INTO usda_commodity (name, api_name, usda_code, created_at, updated_at)
                            VALUES (:name, :api_name, :usda_code, NOW(), NOW())
                        """), {
                            'name': row['commodity_name'],
                            'api_name': row['api_name'],
                            'usda_code': int(row['usda_code'])
                        })

                print(f"✅ Seeded {len(unique_commodities)} USDA commodities")

                # 2. Seed resource_usda_commodity_map table (name-based lookups)
                print("🌱 Seeding resource_usda_commodity_map table...")

                # Clear existing mappings first
                conn.execute(text("DELETE FROM resource_usda_commodity_map"))

                for _, row in mapped_df.iterrows():
                    # Lookup resource_id by name
                    resource_result = conn.execute(text(
                        "SELECT id FROM resource WHERE name = :resource_name"
                    ), {'resource_name': row['resource_name']})
                    resource_row = resource_result.fetchone()

                    if not resource_row:
                        print(f"⚠️  Resource '{row['resource_name']}' not found - skipping")
                        continue

                    resource_id = resource_row[0]

                    # Lookup commodity_id by name
                    commodity_result = conn.execute(text(
                        "SELECT id FROM usda_commodity WHERE name = :commodity_name"
                    ), {'commodity_name': row['commodity_name']})
                    commodity_row = commodity_result.fetchone()

                    if not commodity_row:
                        print(f"⚠️  Commodity '{row['commodity_name']}' not found - skipping")
                        continue

                    commodity_id = commodity_row[0]

                    # Insert mapping with runtime-resolved IDs
                    conn.execute(text("""
                        INSERT INTO resource_usda_commodity_map (
                            resource_id, usda_commodity_id, match_tier, note, created_at, updated_at
                        )
                        VALUES (:resource_id, :usda_commodity_id, :match_tier, :note, NOW(), NOW())
                    """), {
                        'resource_id': resource_id,
                        'usda_commodity_id': commodity_id,
                        'match_tier': row['match_tier'],
                        'note': row['note']
                    })

                print(f"✅ Seeded {len(mapped_df)} resource-commodity mappings")

                # Commit transaction
                trans.commit()
                print("🎉 Successfully seeded commodity mappings from CSV!")
                return True

            except Exception as e:
                trans.rollback()
                print(f"❌ Error seeding commodity mappings: {e}")
                return False

    except Exception as e:
        print(f"❌ Error in seed_commodity_mappings_from_csv: {e}")
        return False


def check_seeding_prerequisites(engine=None) -> dict:
    """
    Check if prerequisite tables (resource, primary_ag_product) are populated.

    Returns:
        dict: Status of prerequisite tables
    """
    try:
        if engine is None:
            engine = get_local_engine()

        with engine.connect() as conn:
            # Check resource table
            resource_count = conn.execute(text("SELECT COUNT(*) FROM resource")).scalar()

            # Check primary_ag_product table
            primary_ag_count = conn.execute(text("SELECT COUNT(*) FROM primary_ag_product")).scalar()

            return {
                'resource_count': resource_count,
                'primary_ag_product_count': primary_ag_count,
                'prerequisites_met': resource_count > 0 and primary_ag_count > 0
            }

    except Exception as e:
        print(f"Error checking prerequisites: {e}")
        return {
            'resource_count': 0,
            'primary_ag_product_count': 0,
            'prerequisites_met': False,
            'error': str(e)
        }


if __name__ == "__main__":
    # Check prerequisites first
    status = check_seeding_prerequisites()
    print(f"Prerequisites check: {status}")

    if status['prerequisites_met']:
        success = seed_commodity_mappings_from_csv()
        print(f"Seeding result: {'✅ Success' if success else '❌ Failed'}")
    else:
        print("❌ Prerequisites not met - resource and primary_ag_product tables must be populated first")
        print("   Run the full ETL pipeline (pixi run run-etl) to populate these tables")
