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

    with open(file_path, 'w') as f:
        f.write(new_content)

def generate_sqla():
    """
    Generates SQLAlchemy models from LinkML schema modules.
    """
    # Script is now at: resources/linkml/scripts/generate_test_sqla.py
    script_dir = Path(__file__).parent
    linkml_dir = script_dir.parent / "test_schemas"  # resources/linkml/test_schemas
    project_root = script_dir.parent.parent  # ca-biositing/
    output_dir = project_root / "src/ca_biositing/datamodels/ca_biositing/datamodels/schemas/generated_test"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Clean output directory
    print(f"Cleaning output directory: {output_dir}")
    for file in output_dir.glob("*.py"):
        if file.name != "__init__.py":
            file.unlink()

    # Generate for modules
    for yaml_file in linkml_dir.glob("*.yaml"):
        module_name = yaml_file.stem
        output_file = output_dir / f"{module_name}.py"
        print(f"Generating {output_file} from {yaml_file}...")

        cmd = [
            "python", "-m", "linkml.generators.sqlalchemygen",
            "--mergeimports",
            str(yaml_file)
        ]

        with open(output_file, "w") as f:
            subprocess.run(cmd, stdout=f, check=True)

        post_process_file(output_file)

    print("Generation complete.")

if __name__ == "__main__":
    generate_sqla()
