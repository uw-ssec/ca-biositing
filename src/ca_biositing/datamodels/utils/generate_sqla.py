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
    # Convert ForeignKey references from class names to table names
    # Matches: ForeignKey('SomeClass.column') -> ForeignKey('some_class.column')
    def replace_foreign_key(match):
        fk_content = match.group(0)
        # Extract the table/class name and column name from inside the quotes
        inner_match = re.search(r"ForeignKey\('([A-Za-z0-9]+)\.([A-Za-z0-9]+)'\)", fk_content)
        if inner_match:
            class_name = inner_match.group(1)
            column_name = inner_match.group(2)
            table_name = to_snake_case(class_name)
            return fk_content.replace(f"'{class_name}.{column_name}'", f"'{table_name}.{column_name}'")
        return fk_content

    # Apply to all ForeignKey occurrences
    new_content = re.sub(r"ForeignKey\('[^']+\.[^']+'\)", replace_foreign_key, new_content)

    # Inject the Base import
    new_content = "from ...database import Base\n\n" + new_content

        # Inject the Base import
    new_content = "from ...database import Base\n\n" + new_content

    # Remove the line that redefines Base
    new_content = re.sub(r"Base = declarative_base\(\)\n", "", new_content)

    # Remove the unused import if present
    new_content = re.sub(r"from sqlalchemy\.orm import declarative_base\n", "", new_content)

    with open(file_path, 'w') as f:
        f.write(new_content)


def generate_sqla():
    """
    Generates SQLAlchemy models from LinkML schema modules.
    """
    base_dir = Path(__file__).parent.parent
    linkml_dir = base_dir / "ca_biositing/datamodels/linkml"
    modules_dir = linkml_dir / "modules"
    output_dir = base_dir / "ca_biositing/datamodels/schemas/generated"

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
