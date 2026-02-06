from typing import List, Optional
import sys
import os
from sqlalchemy import text, create_engine
from sqlmodel import Session, select
from .reviewed_api_mappings import get_api_name


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
            # Load from .env (now has correct localhost credentials)
            db_url = os.getenv(
                "DATABASE_URL",
                "postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db"
            )
            engine = create_engine(db_url, echo=False)

        # Use raw SQLAlchemy connection to get USDA codes for mapped commodities
        from sqlalchemy import text as sql_text
        with engine.connect() as conn:
            # First check if usda_commodity table has any data
            count_result = conn.execute(sql_text("SELECT COUNT(*) FROM usda_commodity"))
            count = count_result.scalar()

            if count == 0:
                print("⚠️ USDA commodity table is empty - no commodities to map")
                print("   This likely means the coworker's ETL flow hasn't populated the database yet")
                print("   You need to run: pixi run run-etl")
                print("   before running USDA ingestion")
                return []

            # Return ONLY commodities that are mapped to resources
            # Prefer api_name when available (after schema migration)
            if use_api_names:
                # Try to get api_name first (will work after schema migration)
                try:
                    result = conn.execute(sql_text("""
                        SELECT DISTINCT
                            COALESCE(uc.api_name, uc.name) as commodity_name
                        FROM usda_commodity uc
                        JOIN resource_usda_commodity_map rcm ON uc.id = rcm.usda_commodity_id
                        WHERE rcm.match_tier != 'UNMAPPED'
                          AND COALESCE(uc.api_name, uc.name) IS NOT NULL
                        ORDER BY commodity_name
                    """))
                    names = [row[0] for row in result.fetchall()]
                except Exception as api_error:
                    # Fallback if api_name column doesn't exist yet
                    print(f"⚠️  api_name column not available yet, using name with mapping fallback")
                    result = conn.execute(sql_text("""
                        SELECT DISTINCT uc.name
                        FROM usda_commodity uc
                        JOIN resource_usda_commodity_map rcm ON uc.id = rcm.usda_commodity_id
                        WHERE rcm.match_tier != 'UNMAPPED'
                          AND uc.name IS NOT NULL
                        ORDER BY uc.name
                    """))
                    db_names = [row[0] for row in result.fetchall()]
                    # Apply mapping function as fallback
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
