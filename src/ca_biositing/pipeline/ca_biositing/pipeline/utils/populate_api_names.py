#!/usr/bin/env python3
"""
Populate api_name field in usda_commodity table with official API names.

This script should be run after the schema migration to populate the new
api_name column with the correct values for API compatibility.
"""

import os
from sqlalchemy import create_engine, text
from datetime import datetime, UTC
from .reviewed_api_mappings import OFFICIAL_API_MAPPINGS

def populate_api_names(engine=None, dry_run=False):
    """
    Populate the api_name field for existing commodity records.

    Args:
        engine: SQLAlchemy engine (optional)
        dry_run: If True, show what would be updated without making changes

    Returns:
        Dict with update statistics
    """
    if engine is None:
        db_url = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db"
        )
        engine = create_engine(db_url, echo=False)

    stats = {
        'total_commodities': 0,
        'updated_commodities': 0,
        'exact_matches': 0,
        'mapped_commodities': 0,
        'unmapped_commodities': 0,
        'errors': []
    }

    try:
        with engine.connect() as conn:
            # First, get all current commodities
            result = conn.execute(text("""
                SELECT id, name, api_name
                FROM usda_commodity
                ORDER BY name
            """))
            commodities = result.fetchall()
            stats['total_commodities'] = len(commodities)

            print(f"Found {len(commodities)} commodities in database")
            print("\nAPI Name Population Plan:")
            print("=" * 50)

            updates = []
            current_time = datetime.now(UTC)

            for commodity_id, name, existing_api_name in commodities:
                # Skip if api_name already populated
                if existing_api_name:
                    print(f"  SKIP: {name:<25} (already has api_name: {existing_api_name})")
                    continue

                # Get the API name from our mapping
                api_name = OFFICIAL_API_MAPPINGS.get(name, name)

                if api_name == name:
                    # Exact match - no mapping needed
                    status = "EXACT"
                    stats['exact_matches'] += 1
                else:
                    # Mapping applied
                    status = "MAPPED"
                    stats['mapped_commodities'] += 1

                print(f"  {status}: {name:<25} → {api_name}")

                if not dry_run:
                    updates.append({
                        'id': commodity_id,
                        'api_name': api_name,
                        'updated_at': current_time
                    })

            # Perform updates if not dry run
            if not dry_run and updates:
                print(f"\nExecuting {len(updates)} updates...")

                with conn.begin():  # Transaction
                    for update in updates:
                        conn.execute(text("""
                            UPDATE usda_commodity
                            SET api_name = :api_name,
                                updated_at = :updated_at
                            WHERE id = :id
                        """), update)

                stats['updated_commodities'] = len(updates)
                print(f"✅ Updated {len(updates)} commodity records")

            elif dry_run:
                print(f"\n🔍 DRY RUN: Would update {len(updates)} records")
                stats['updated_commodities'] = len(updates)

    except Exception as e:
        error_msg = f"Error updating api_names: {e}"
        stats['errors'].append(error_msg)
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()

    return stats

def validate_api_names(engine=None):
    """
    Validate that all mapped commodities have api_name populated.

    Returns:
        Dict with validation results
    """
    if engine is None:
        db_url = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db"
        )
        engine = create_engine(db_url, echo=False)

    results = {
        'total_mapped': 0,
        'with_api_name': 0,
        'missing_api_name': [],
        'validation_passed': True
    }

    try:
        with engine.connect() as conn:
            # Get mapped commodities and their api_name status
            result = conn.execute(text("""
                SELECT DISTINCT uc.name, uc.api_name
                FROM usda_commodity uc
                JOIN resource_usda_commodity_map rcm ON uc.id = rcm.usda_commodity_id
                WHERE rcm.match_tier != 'UNMAPPED'
                ORDER BY uc.name
            """))

            for name, api_name in result.fetchall():
                results['total_mapped'] += 1
                if api_name:
                    results['with_api_name'] += 1
                else:
                    results['missing_api_name'].append(name)
                    results['validation_passed'] = False

    except Exception as e:
        print(f"Validation error: {e}")
        results['validation_passed'] = False

    return results

if __name__ == "__main__":
    import sys

    dry_run = "--dry-run" in sys.argv

    print("USDA COMMODITY API NAME POPULATION")
    print("=" * 40)

    # Run population
    stats = populate_api_names(dry_run=dry_run)

    print(f"\n📊 STATISTICS:")
    print(f"  Total commodities: {stats['total_commodities']}")
    print(f"  Updated: {stats['updated_commodities']}")
    print(f"  Exact matches: {stats['exact_matches']}")
    print(f"  Mapped: {stats['mapped_commodities']}")

    if stats['errors']:
        print(f"  Errors: {len(stats['errors'])}")
        for error in stats['errors']:
            print(f"    - {error}")

    # Validate results
    if not dry_run:
        print(f"\n🔍 VALIDATION:")
        validation = validate_api_names()
        print(f"  Mapped commodities: {validation['total_mapped']}")
        print(f"  With api_name: {validation['with_api_name']}")

        if validation['missing_api_name']:
            print(f"  Missing api_name: {validation['missing_api_name']}")

        if validation['validation_passed']:
            print("  ✅ All mapped commodities have api_name")
        else:
            print("  ❌ Some commodities missing api_name")

    print("\nTo run actual updates: python populate_api_names.py")
    print("To preview changes: python populate_api_names.py --dry-run")
