#!/usr/bin/env python3
"""Fix all incorrect tablenames in generated SQLModel files."""

import re
from pathlib import Path

# Get all tablenames from the original generated file
def extract_tablenames(generated_file: Path):
    """Extract class-to-tablename mapping from the original generated file."""
    mapping = {}
    with open(generated_file) as f:
        content = f.read()

    # Find all class definitions and their tablenames
    pattern = r"class (\w+)\(.*?\):\s*\"\"\".*?\"\"\"\s*__tablename__\s*=\s*'([^']+)'"
    matches = re.findall(pattern, content, re.DOTALL)

    for class_name, tablename in matches:
        if class_name not in ["BaseEntity", "LookupBase", "Aim1RecordBase", "Aim2RecordBase", "LandiqRecordView"]:
            mapping[class_name] = tablename

    return mapping

def fix_model_file(filepath: Path, tablename_mapping: dict):
    """Fix tablenames in a single model file."""
    content = filepath.read_text()
    modified = False

    # Find class definitions and fix their tablenames
    for class_name, correct_tablename in tablename_mapping.items():
        # Pattern to match: class ClassName(...): followed by __tablename__ = "..."
        pattern = rf'(class {class_name}\([^)]+\):[^\n]*\n(?:[^\n]*\n)*?\s*__tablename__\s*=\s*")([^"]+)(")'

        def replacer(match):
            nonlocal modified
            current_tablename = match.group(2)
            if current_tablename != correct_tablename:
                modified = True
                print(f"  {filepath.name}: {class_name}.{current_tablename} -> {correct_tablename}")
                return match.group(1) + correct_tablename + match.group(3)
            return match.group(0)

        content = re.sub(pattern, replacer, content)

    if modified:
        filepath.write_text(content)
        return True
    return False

def main():
    project_root = Path(__file__).parent.parent
    generated_file = project_root / "src/ca_biositing/datamodels/ca_biositing/datamodels/schemas/generated/ca_biositing.py"
    models_dir = project_root / "src/ca_biositing/datamodels/ca_biositing/datamodels/models"

    print("🔍 Extracting correct tablenames from generated file...")
    tablename_mapping = extract_tablenames(generated_file)
    print(f"   Found {len(tablename_mapping)} table mappings\n")

    print("🔧 Fixing tablenames in SQLModel files...")
    fixed_count = 0
    for pyfile in models_dir.rglob("*.py"):
        if pyfile.name == "__init__.py" or pyfile.name == "base.py":
            continue

        if fix_model_file(pyfile, tablename_mapping):
            fixed_count += 1

    print(f"\n✅ Fixed {fixed_count} files")

if __name__ == "__main__":
    main()
