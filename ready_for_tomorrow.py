#!/usr/bin/env python3
"""
Quick test script for tomorrow - verify everything is working.

Run this to quickly test the API mapping and ETL readiness.
"""

def test_api_mappings():
    """Test the API mapping logic."""
    try:
        from src.ca_biositing.pipeline.ca_biositing.pipeline.utils.reviewed_api_mappings import (
            get_api_name, get_all_api_names, OFFICIAL_API_MAPPINGS
        )

        print("✅ API Mapping Module Loaded")
        print(f"   - {len(OFFICIAL_API_MAPPINGS)} commodities mapped")
        print(f"   - {len(get_all_api_names())} unique API names")

        # Test a few key mappings
        test_cases = [
            ('ALL GRAPES', 'GRAPES'),
            ('CORN  FOR SILAGE', 'SILAGE'),
            ('ALMONDS', 'ALMONDS')
        ]

        for db_name, expected in test_cases:
            actual = get_api_name(db_name)
            if actual == expected:
                print(f"   ✓ {db_name} → {actual}")
            else:
                print(f"   ❌ {db_name} → {actual} (expected {expected})")

        return True

    except Exception as e:
        print(f"❌ API Mapping Test Failed: {e}")
        return False

def test_database_connection():
    """Test database connection."""
    try:
        import subprocess
        result = subprocess.run(['pixi', 'run', 'service-status'],
                              capture_output=True, text=True, timeout=10)

        if 'Up' in result.stdout and 'healthy' in result.stdout:
            print("✅ Database Services Running")
            return True
        else:
            print("❌ Database Services Not Ready")
            print("   Run: pixi run start-services")
            return False

    except Exception as e:
        print(f"❌ Database Connection Test Failed: {e}")
        return False

def main():
    print("🚀 TOMORROW'S READINESS CHECK")
    print("=" * 30)

    all_good = True

    # Test API mappings
    if not test_api_mappings():
        all_good = False

    print()

    # Test database
    if not test_database_connection():
        all_good = False

    print()

    if all_good:
        print("🎉 READY FOR TOMORROW!")
        print("Next steps:")
        print("1. pixi run teardown-services-volumes  # Fresh database")
        print("2. pixi run start-services             # Start clean")
        print("3. pixi run migrate                    # Apply schema")
        print("4. Run populate_api_names.py           # Add API names")
        print("5. Test ETL with improved mappings")
    else:
        print("⚠️  Need to fix issues before tomorrow")

    return all_good

if __name__ == "__main__":
    main()
