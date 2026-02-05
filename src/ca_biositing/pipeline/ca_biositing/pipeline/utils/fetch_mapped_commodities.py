from typing import List, Optional
import sys
import os
from sqlalchemy import text, create_engine
from sqlmodel import Session, select


def get_mapped_commodity_ids(engine=None) -> Optional[List[str]]:
    """
    Get USDA commodity NAMES from database for API queries.

    The USDA QuickStats API expects commodity names (e.g., "CORN", "WHEAT")
    not codes. This function returns names from the usda_commodity table.

    Returns:
        List of USDA commodity names (e.g., ["CORN", "WHEAT", ...])
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
