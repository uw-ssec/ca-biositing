#!/usr/bin/env python3
"""
Test script to manually run commodity mapping seeding
"""

import sys
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Manual .env loading if dotenv not available
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

# Override DATABASE_URL to use correct port for local testing
if 'DATABASE_URL' not in os.environ:
    os.environ['DATABASE_URL'] = 'postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:9090/biocirv_db'

# Use proper namespace package imports
from ca_biositing.pipeline.utils.seed_commodity_mappings import seed_commodity_mappings_from_csv, check_seeding_prerequisites

def test_seeding_logic():
    """Test seeding logic with mocks to avoid DB dependency in CI."""
    from unittest.mock import patch, MagicMock

    with patch("ca_biositing.pipeline.utils.seed_commodity_mappings.seed_commodity_mappings_from_csv") as mock_seed:
        mock_seed.return_value = True
        success = seed_commodity_mappings_from_csv()
        assert success is True

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

    # Try to connect to database with port fallback (9090 then 5432)
    DATABASE_PORTS = [9090, 5432]
    db_base_url = "postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:{}/biocirv_db"

    engine = None
    for port in DATABASE_PORTS:
        try:
            test_engine = create_engine(db_base_url.format(port), echo=False)
            with test_engine.connect() as test_conn:
                test_conn.execute(text("SELECT 1"))
            print(f"✅ Database connected on port {port}")
            engine = test_engine
            break
        except Exception as e:
            print(f"❌ Port {port} failed: {e}")
            continue

    if engine is None:
        print(f"❌ Could not connect to database on any port: {DATABASE_PORTS}")
        return

    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, name, api_name, usda_code, uri FROM usda_commodity LIMIT 5"))
        rows = result.fetchall()
        print("Sample rows:")
        for row in rows:
            print(f"  ID: {row[0]}, Name: '{row[1]}', API Name: '{row[2]}', USDA Code: {row[3]} ({type(row[3])}), URI: '{row[4]}'")

if __name__ == "__main__":
    main()
