import os
import re
import subprocess
from pathlib import Path

def to_snake_case(name):
    """Converts PascalCase to snake_case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def post_process_file(file_path):
    """
    Post-processes the generated file to convert table names to snake_case.
    """
    with open(file_path, 'r') as f:
        content = f.read()

    # Regex to find __tablename__ assignments
    # Matches: __tablename__ = 'SomeName'
    pattern = r"__tablename__ = '([A-Za-z0-9]+)'"

    def replace_tablename(match):
        original_name = match.group(1)
        snake_name = to_snake_case(original_name)
        return f"__tablename__ = '{snake_name}'"

    new_content = re.sub(pattern, replace_tablename, content)

    # Convert ForeignKey references from class names to table names
    # Matches: ForeignKey('SomeClass.id') -> ForeignKey('some_class.id')
    def replace_foreign_key(match):
        fk_content = match.group(0)
        # Extract the table/class name and column name from inside the quotes
        inner_match = re.search(r"ForeignKey\('([A-Za-z0-9]+)\.([A-Za-z0-9]+)'\)", fk_content)
        if inner_match:
            class_name = inner_match.group(1)
            column_name = inner_match.group(2)

            # CUSTOM FIX: Force dataset_id to point to 'dataset' table, not 'data_source'
            # This applies to Observation and all Record classes
            # If the user changes range to 'integer', this block won't be reached as there's no ForeignKey
            if class_name == 'DataSource' and 'dataset_id' in match.string[max(0, match.start()-100):match.end()]:
                table_name = 'dataset'
            else:
                table_name = to_snake_case(class_name)

            return fk_content.replace(f"'{class_name}.{column_name}'", f"'{table_name}.{column_name}'")
        return fk_content

    # Apply to all ForeignKey occurrences
    new_content = re.sub(r"ForeignKey\('[^']+\.[^']+'\)", replace_foreign_key, new_content)

    # Inject the Base import and other necessary imports
    new_content = "from ...database import Base\nfrom sqlalchemy import text, Index\n\n" + new_content

    # Remove the line that redefines Base
    new_content = re.sub(r"Base = declarative_base\(\)\n", "", new_content)

    # Remove the unused import if present
    new_content = re.sub(r"from sqlalchemy\.orm import declarative_base\n", "", new_content)

    # Inject UniqueConstraint for record_id on specific classes
    # This ensures Alembic detects them and they are part of the SQLAlchemy model
    target_classes = [
        'Observation', 'LandiqRecord', 'Aim1RecordBase', 'Aim2RecordBase', 'AutoclaveRecord',
        'CalorimetryRecord', 'CompositionalRecord', 'FermentationRecord',
        'FtnirRecord', 'GasificationRecord', 'IcpRecord', 'PretreatmentRecord',
        'ProximateRecord', 'RgbRecord', 'UltimateRecord', 'XrdRecord', 'XrfRecord'
    ]

    for cls_name in target_classes:
        # LinkML generator usually puts record_id as a regular Column(Text())
        # We replace the existing record_id definition to include unique=True
        # We also handle cases where it might be marked as primary_key=True by LinkML
        record_id_pattern = rf"(class {cls_name}\(.*?record_id = Column\(Text\(\))([^)]*)\)"

        def add_unique_param(m):
            prefix = m.group(1)
            params = m.group(2)
            if "unique=True" in params:
                return m.group(0)
            # Add unique=True and ensure nullable=False
            new_params = params
            if "nullable=False" not in params:
                new_params += ", nullable=False"
            return f"{prefix}{new_params}, unique=True)"

        new_content = re.sub(record_id_pattern, add_unique_param, new_content, flags=re.DOTALL)

    # CUSTOM FIX: Preserve unique_geom_dataset_md5 index on Polygon
    # This index uses a functional expression md5(geom) which LinkML doesn't support
    # We inject it into __table_args__ later in the script to avoid conflicts

    # Ensure 'text' and 'Index' are imported from sqlalchemy for functional indexes
    # (Handled by global injection at top of file now)

    # CUSTOM FIX: Ensure 'id' is the Primary Key and autoincrements
    # This aligns the code with the physical DB structure where BaseEntity.id is the PK.

    # 1. Remove primary_key=True from record_id to avoid composite primary keys
    # Composite keys disable autoincrement on 'id' by default in SQLAlchemy.
    # We use a regex to handle variations in whitespace or other parameters.
    new_content = re.sub(
        r"(record_id = Column\(Text\(\)), primary_key=True",
        r"\1",
        new_content
    )

    # Also remove record_id from any PrimaryKeyConstraint if LinkML injected it
    new_content = re.sub(
        r"PrimaryKeyConstraint\(([^)]*?)'record_id',?\s*([^)]*?)\)",
        r"PrimaryKeyConstraint(\1\2)",
        new_content
    )
    # Clean up trailing commas in PrimaryKeyConstraint
    new_content = new_content.replace(", )", ")")

    # 2. Ensure 'id' columns that are Integers and NOT ForeignKeys have primary_key=True and autoincrement=True
    # We use a strict regex to target the 'id' column specifically and avoid duplicates.
    def add_id_pk_params(m):
        prefix = m.group(1)
        params = m.group(2)
        suffix = m.group(3)
        if "primary_key=True" not in params:
            params = ", primary_key=True" + params
        if "autoincrement=True" not in params:
            params = ", autoincrement=True" + params
        return f"{prefix}{params}{suffix}"

    new_content = re.sub(
        r"(\s+id = Column\(Integer\(\))((?!, ForeignKey)[^)]*)(\))",
        add_id_pk_params,
        new_content
    )

    # 3. FIX: Ensure tables without an 'id' column (like Place or Infrastructure) still have a Primary Key
    # We look for classes that have no primary_key=True after our previous steps
    class_blocks = re.split(r"(class \w+\(Base\):|class \w+\(BaseEntity\):|class \w+\(LookupBase\):)", new_content)
    processed_blocks = []
    for i in range(len(class_blocks)):
        block = class_blocks[i]
        # If this is a class body and it doesn't have a primary key
        if i > 0 and "Column(" in block and "primary_key=True" not in block:
            # Priority 1: Look for a column that looks like a primary key (e.g., biodiesel_plant_id)
            # but exclude ForeignKeys
            pk_match = re.search(r"(\w+_id = Column\((?:Integer|Text)\(\), nullable=False)([^)]*)(\))", block)
            if pk_match:
                block = block.replace(pk_match.group(0), f"{pk_match.group(1)}, primary_key=True{pk_match.group(2)}{pk_match.group(3)}")
            else:
                # Priority 2: Fallback to the very first column
                block = re.sub(r"(Column\([^)]+)(?=\))", r"\1, primary_key=True", block, count=1)
        processed_blocks.append(block)
    new_content = "".join(processed_blocks)

    # 4. Add extend_existing=True to all classes to prevent MetaData conflicts in Prefect
    # This fixes "Table 'base_entity' is already defined for this MetaData instance"
    # SPECIAL CASE: Polygon needs the functional unique index
    def add_table_args(m):
        tablename_line = m.group(1)
        tablename = re.search(r"'([^']+)'", tablename_line).group(1)

        if tablename == 'polygon':
            return f"{tablename_line}\n    __table_args__ = (\n        Index('unique_geom_dataset_md5', text('md5(geom)'), 'dataset_id', unique=True),\n        {{'extend_existing': True}}\n    )"
        else:
            return f"{tablename_line}\n    __table_args__ = {{'extend_existing': True}}"

    new_content = re.sub(
        r"(__tablename__ = '.*?')",
        add_table_args,
        new_content
    )

    # Final safety check: if sa.text still exists anywhere (e.g. in other manual injections), fix it
    new_content = new_content.replace("sa.text(", "text(")

    with open(file_path, 'w') as f:
        f.write(new_content)


def generate_sqla():
    """
    Generates SQLAlchemy models from LinkML schema modules.
    """
    # Script is now at: resources/linkml/scripts/generate_sqla.py
    script_dir = Path(__file__).parent
    linkml_dir = script_dir.parent  # resources/linkml/
    project_root = linkml_dir.parent.parent  # ca-biositing/

    modules_dir = linkml_dir / "modules"
    output_dir = project_root / "src/ca_biositing/datamodels/ca_biositing/datamodels/schemas/generated"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Clean output directory recursively
    print(f"Cleaning output directory: {output_dir}")
    for f in output_dir.glob('**/*.py'):
        if f.name != '__init__.py':
            f.unlink()

    # Generate for modules

    # Generate for main schema
    main_yaml = linkml_dir / "ca_biositing.yaml"
    main_output = output_dir / "ca_biositing.py"
    print(f"Generating {main_output} from {main_yaml}...")

    cmd = [
        "python", "-m", "linkml.generators.sqlalchemygen",
        "--mergeimports",
        str(main_yaml)
    ]

    with open(main_output, "w") as f:
        subprocess.run(cmd, stdout=f, check=True)

    post_process_file(main_output)

    print("Generation complete.")

if __name__ == "__main__":
    generate_sqla()
