from typing import List, Optional
import sys
from sqlalchemy import text
from sqlmodel import Session, select

# Optional fallback import
try:
    from .reviewed_api_mappings import get_api_name
    HAS_API_MAPPINGS_FALLBACK = True
except ImportError:
    HAS_API_MAPPINGS_FALLBACK = False
    def get_api_name(name):
        return name  # Identity fallback


def get_mapped_commodity_ids(engine=None, use_api_names=True) -> Optional[List[str]]:
    """
    Get USDA commodity NAMES from database for API queries.

    The USDA QuickStats API expects commodity names (e.g., "CORN", "WHEAT")
    not codes. This function returns names from the usda_commodity table,
    preferring api_name when available for proper API compatibility.

    Args:
        engine: SQLAlchemy engine (optional, will create if None)
        use_api_names: Whether to use api_name column when available (default True)

    Returns:
        List of USDA commodity names ready for API calls (e.g., ["CORN", "WHEAT", ...])
    """
    try:
        if engine is None:
            from ca_biositing.pipeline.utils.engine import get_engine
            engine = get_engine()

        # Use raw SQLAlchemy connection to get USDA codes for mapped commodities
        from sqlalchemy import text as sql_text
        with engine.connect() as conn:
            # First check if usda_commodity table has any data
            count_result = conn.execute(sql_text("SELECT COUNT(*) FROM usda_commodity"))
            count = count_result.scalar()

            if count == 0:
                print("⚠️ USDA commodity table is empty - attempting auto-seed from CSV...")
                # Try to auto-seed from CSV mapping file
                try:
                    from .seed_commodity_mappings import seed_commodity_mappings_from_csv, check_seeding_prerequisites

                    # Check if prerequisite tables are populated
                    prereq_status = check_seeding_prerequisites(engine)
                    if not prereq_status['prerequisites_met']:
                        print(f"❌ Prerequisites not met: resource table has {prereq_status['resource_count']} rows, primary_ag_product has {prereq_status['primary_ag_product_count']} rows")
                        print("   Run the full ETL pipeline first to populate resource and primary_ag_product tables")
                        return []

                    # Attempt seeding
                    print("🌱 Auto-seeding commodity mappings from CSV...")
                    if seed_commodity_mappings_from_csv(engine=engine):
                        print("✅ Auto-seeding successful! Retrying commodity lookup...")
                        # Retry count after seeding
                        count_result = conn.execute(sql_text("SELECT COUNT(*) FROM usda_commodity"))
                        count = count_result.scalar()
                        print(f"📊 USDA commodity table now has {count} commodities")
                    else:
                        print("❌ Auto-seeding failed")
                        return []

                except ImportError as e:
                    print(f"❌ Could not import seeding module: {e}")
                    return []
                except Exception as e:
                    print(f"❌ Auto-seeding error: {e}")
                    return []

            # Return ONLY commodities that are mapped to resources
            # Prefer api_name when available (after schema migration)
            if use_api_names:
                # Try to get api_name first (will work after schema migration)
                try:
                    result = conn.execute(sql_text("""
                        SELECT DISTINCT uc.api_name as commodity_name
                        FROM usda_commodity uc
                        JOIN resource_usda_commodity_map rcm ON uc.id = rcm.usda_commodity_id
                        WHERE rcm.match_tier != 'UNMAPPED'
                          AND uc.api_name IS NOT NULL
                          AND uc.api_name != ''
                        ORDER BY commodity_name
                    """))
                    names = [row[0] for row in result.fetchall()]
                    if not names:
                        print("🔍 No mapped commodities found after seeding - continuing with empty list")
                except Exception as api_error:
                    # Fallback if api_name column doesn't exist yet
                    fallback_msg = "using name with mapping fallback" if HAS_API_MAPPINGS_FALLBACK else "using names directly (no mappings available)"
                    print(f"⚠️  api_name column not available yet, {fallback_msg}")
                    result = conn.execute(sql_text("""
                        SELECT DISTINCT uc.name
                        FROM usda_commodity uc
                        JOIN resource_usda_commodity_map rcm ON uc.id = rcm.usda_commodity_id
                        WHERE rcm.match_tier != 'UNMAPPED'
                          AND uc.name IS NOT NULL
                        ORDER BY uc.name
                    """))
                    db_names = [row[0] for row in result.fetchall()]
                    # Apply mapping function as fallback (or identity if not available)
                    names = [get_api_name(name) for name in db_names]
            else:
                # Use database names directly
                result = conn.execute(sql_text("""
                    SELECT DISTINCT uc.name
                    FROM usda_commodity uc
                    JOIN resource_usda_commodity_map rcm ON uc.id = rcm.usda_commodity_id
                    WHERE rcm.match_tier != 'UNMAPPED'
                      AND uc.name IS NOT NULL
                    ORDER BY uc.name
                """))
                names = [row[0] for row in result.fetchall()]
            return names if names else []
    except Exception as e:
        print(f"Error querying mapped commodities: {e}")
        import traceback
        traceback.print_exc()
        return []


if __name__ == "__main__":
    ids = get_mapped_commodity_ids()
    print(f"Mapped USDA commodity IDs: {ids}")
