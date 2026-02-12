#!/usr/bin/env python3
"""Fix infrastructure tablenames in generated SQLModel files."""

import re
from pathlib import Path

# Mapping of incorrect to correct tablenames
TABLENAME_FIXES = {
    "infrastructurebiosolidsfacilities": "infrastructure_biosolids_facilities",
    "infrastructurecafomanurelocations": "infrastructure_cafo_manure_locations",
    "infrastructurecombustionplants": "infrastructure_combustion_plants",
    "infrastructuredistrictenergysystems": "infrastructure_district_energy_systems",
    "infrastructureethanolbiorefineries": "infrastructure_ethanol_biorefineries",
    "infrastructurefoodprocessingfacilities": "infrastructure_food_processing_facilities",
    "infrastructurelandfills": "infrastructure_landfills",
    "infrastructurelivestockanaerobicdigesters": "infrastructure_livestock_anaerobic_digesters",
}

def fix_file(filepath: Path):
    """Fix tablenames in a file."""
    content = filepath.read_text()
    modified = False

    for wrong, correct in TABLENAME_FIXES.items():
        if f'__tablename__ = "{wrong}"' in content:
            content = content.replace(f'__tablename__ = "{wrong}"', f'__tablename__ = "{correct}"')
            modified = True
            print(f"✓ Fixed {filepath.name}: {wrong} -> {correct}")

    if modified:
        filepath.write_text(content)

def main():
    project_root = Path(__file__).parent.parent
    infrastructure_dir = project_root / "src/ca_biositing/datamodels/ca_biositing/datamodels/models/infrastructure"

    print("🔧 Fixing infrastructure tablenames...")
    for pyfile in infrastructure_dir.glob("*.py"):
        if pyfile.name != "__init__.py":
            fix_file(pyfile)

    print("\n✅ Done!")

if __name__ == "__main__":
    main()
