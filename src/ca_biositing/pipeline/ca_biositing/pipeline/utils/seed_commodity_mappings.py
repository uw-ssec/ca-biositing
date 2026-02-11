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
from sqlalchemy import text, create_engine


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
            db_url = os.getenv(
                "DATABASE_URL",
                "postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db"
            )
            engine = create_engine(db_url, echo=False)

        # Default CSV path
        if csv_path is None:
            current_dir = os.path.dirname(__file__)
            csv_path = os.path.join(current_dir, "commodity_mappings_corrected.csv")

        if not os.path.exists(csv_path):
            print(f"❌ Mapping CSV file not found: {csv_path}")
            return False

        # Read CSV mapping file
        print(f"📊 Reading mapping file: {csv_path}")
        df = pd.read_csv(csv_path)

        # Filter out unmapped entries
        mapped_df = df[df['match_tier'] != 'UNMAPPED'].copy()
        print(f"📊 Found {len(mapped_df)} mapped commodities (excluding {len(df) - len(mapped_df)} unmapped)")

        with engine.connect() as conn:
            # Start transaction
            trans = conn.begin()

            try:
                # 1. Seed usda_commodity table (unique commodities only)
                print("🌱 Seeding usda_commodity table...")
                unique_commodities = mapped_df.drop_duplicates('usda_commodity_id')[
                    ['usda_commodity_id', 'commodity_name', 'api_name', 'usda_code', 'uri']
                ].copy()

                for _, row in unique_commodities.iterrows():
                    conn.execute(text("""
                        INSERT INTO usda_commodity (id, name, api_name, usda_code, uri, created_at, updated_at)
                        VALUES (:id, :name, :api_name, :usda_code, :uri, NOW(), NOW())
                        ON CONFLICT (id) DO UPDATE SET
                            name = EXCLUDED.name,
                            api_name = EXCLUDED.api_name,
                            usda_code = EXCLUDED.usda_code,
                            uri = EXCLUDED.uri,
                            updated_at = NOW()
                    """), {
                        'id': int(row['usda_commodity_id']),
                        'name': row['commodity_name'],
                        'api_name': row['api_name'],  # Use correct api_name from CSV
                        'usda_code': int(row['usda_code']),  # Ensure integer
                        'uri': row['uri']
                    })

                print(f"✅ Seeded {len(unique_commodities)} USDA commodities")

                # 2. Seed resource_usda_commodity_map table
                print("🌱 Seeding resource_usda_commodity_map table...")

                for _, row in mapped_df.iterrows():
                    conn.execute(text("""
                        INSERT INTO resource_usda_commodity_map (
                            id, resource_id, usda_commodity_id, match_tier, note, created_at, updated_at
                        )
                        VALUES (:id, :resource_id, :usda_commodity_id, :match_tier, :note, :created_at, :updated_at)
                        ON CONFLICT (id) DO UPDATE SET
                            resource_id = EXCLUDED.resource_id,
                            usda_commodity_id = EXCLUDED.usda_commodity_id,
                            match_tier = EXCLUDED.match_tier,
                            note = EXCLUDED.note,
                            updated_at = EXCLUDED.updated_at
                    """), {
                        'id': int(row['id']),
                        'resource_id': int(row['resource_id']),
                        'usda_commodity_id': int(row['usda_commodity_id']),
                        'match_tier': row['match_tier'],
                        'note': row['note'],
                        'created_at': pd.to_datetime(row['created_at']),
                        'updated_at': pd.to_datetime(row['updated_at'])
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
            db_url = os.getenv(
                "DATABASE_URL",
                "postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db"
            )
            engine = create_engine(db_url, echo=False)

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
