import os
import re
import subprocess
import yaml
from pathlib import Path

def to_snake_case(name):
    """Converts PascalCase to snake_case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def post_process_file(file_path):
    """
    Post-processes the generated file to convert table names to snake_case,
    handle custom schemas, and support materialized views.
    """
    print(f"Post-processing {file_path}")
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

    # Detect classes with sql_schema annotation and add __table_args__
    # We'll use a more robust way by parsing the LinkML files to find which classes have views
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent.parent.parent.parent
    views_dir = base_dir / "resources/linkml/modules/ca_biositing_views"

    print(f"Checking for view definitions in {views_dir}")
    view_configs = {}
    if views_dir.exists():
        for yaml_file in views_dir.glob("*.yaml"):
            print(f"Reading {yaml_file}")
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)
                if 'classes' in data:
                    for class_name, class_data in data['classes'].items():
                        annos = class_data.get('annotations', {})
                        if annos.get('materialized') or annos.get('sql_schema'):
                            view_configs[class_name] = {
                                'schema': annos.get('sql_schema'),
                                'materialized': annos.get('materialized', False),
                                'sql_definition': annos.get('sql_definition', '').strip()
                            }
                            print(f"Found view config for {class_name}: {view_configs[class_name]}")

    for class_name, config in view_configs.items():
        if f"class {class_name}" in new_content:
            print(f"Applying view config to {class_name} in generated code")
            schema = config['schema']
            is_materialized = config['materialized']
            sql = config['sql_definition']

            # Prepare the info dict if it's a materialized view
            info_parts = []
            if is_materialized:
                info_parts.append("'is_materialized_view': True")
            if sql:
                # Use raw string for SQL to handle backslashes correctly
                # We also need to escape triple quotes if they exist in SQL
                safe_sql = sql.replace("'''", r"\'\'\'")
                info_parts.append(f"'sql_definition': r'''{safe_sql}'''")

            info_dict_str = ""
            if info_parts:
                info_dict_str = f"'info': {{{', '.join(info_parts)}}}"

            # Find the class and its __table_args__
            # We use a more flexible regex to find the class and then the next __table_args__
            # This regex looks for the class name and then matches until the first __table_args__
            class_search_pattern = rf"class {class_name}\(.*?\):.*?"
            args_pattern = r"(__table_args__ = )(\{.*?\}|\(.*?\)|\{.*?\})"

            combined_pattern = f"({class_search_pattern})({args_pattern})"

            def update_args(m):
                class_prefix = m.group(1)
                args_prefix = m.group(3)
                existing_dict_str = m.group(4)

                print(f"Updating existing __table_args__ for {class_name}")

                # Check if it's a dict or a tuple
                if existing_dict_str.startswith('{'):
                    # It's a dict like {'extend_existing': True}
                    new_dict_str = existing_dict_str.rstrip('}')
                    if schema:
                        new_dict_str += f", 'schema': '{schema}'"
                    if info_dict_str:
                        new_dict_str += f", {info_dict_str}"
                    new_dict_str += "}"
                    return f"{class_prefix}{args_prefix}{new_dict_str}"
                elif existing_dict_str.startswith('('):
                    # It's a tuple like (Index(...), {'extend_existing': True})
                    # We need to find the dict part of the tuple
                    if '{' in existing_dict_str:
                        new_tuple_str = re.sub(
                            r"(\{.*?\})",
                            lambda m2: m2.group(1).rstrip('}') + (f", 'schema': '{schema}'" if schema else "") + (f", {info_dict_str}" if info_dict_str else "") + "}",
                            existing_dict_str
                        )
                        return f"{class_prefix}{args_prefix}{new_tuple_str}"
                    else:
                        # No dict in tuple? Unusual, but let's append one
                        new_tuple_str = existing_dict_str.rstrip(')')
                        new_dict = "{" + (f"'schema': '{schema}'" if schema else "") + (f", {info_dict_str}" if info_dict_str else "") + "}"
                        new_tuple_str += f", {new_dict})"
                        return f"{class_prefix}{args_prefix}{new_tuple_str}"

                return m.group(0)

            if re.search(combined_pattern, new_content, re.DOTALL):
                new_content = re.sub(combined_pattern, update_args, new_content, count=1, flags=re.DOTALL)
            else:
                # If no __table_args__ found, inject one after class definition
                print(f"No __table_args__ found for {class_name}, injecting new one")
                table_args = "{" + (f"'schema': '{schema}'" if schema else "")
                if info_dict_str:
                    table_args += f", {info_dict_str}"
                table_args += "}"
                new_content = re.sub(
                    rf"(class {class_name}\(.*?\):)",
                    rf"\1\n    __table_args__ = {table_args}",
                    new_content
                )

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
            if class_name == 'DataSource' and 'dataset_id' in match.string[max(0, match.start()-100):match.end()]:
                table_name = 'dataset'
            else:
                table_name = to_snake_case(class_name)

            return fk_content.replace(f"'{class_name}.{column_name}'", f"'{table_name}.{column_name}'")
        return fk_content

    # Apply to all ForeignKey occurrences
    new_content = re.sub(r"ForeignKey\('[^']+\.[^']+'\)", replace_foreign_key, new_content)

    # Inject the Base import
    new_content = "from ...database import Base\n\n" + new_content

    # Remove the line that redefines Base
    new_content = re.sub(r"Base = declarative_base\(\)\n", "", new_content)

    # Remove the unused import if present
    new_content = re.sub(r"from sqlalchemy\.orm import declarative_base\n", "", new_content)

    # Inject UniqueConstraint for record_id on specific classes
    target_classes = [
        'Observation', 'Aim1RecordBase', 'Aim2RecordBase', 'AutoclaveRecord',
        'CalorimetryRecord', 'CompositionalRecord', 'FermentationRecord',
        'FtnirRecord', 'GasificationRecord', 'IcpRecord', 'PretreatmentRecord',
        'ProximateRecord', 'RgbRecord', 'UltimateRecord', 'XrdRecord', 'XrfRecord'
    ]

    for cls_name in target_classes:
        record_id_pattern = rf"(class {cls_name}\(.*?record_id = Column\(Text\(\))([^)]*)\)"

        def add_unique_param(m):
            prefix = m.group(1)
            params = m.group(2)
            if "unique=True" in params:
                return m.group(0)
            new_params = params
            if "nullable=False" not in params:
                new_params += ", nullable=False"
            return f"{prefix}{new_params}, unique=True)"

        new_content = re.sub(record_id_pattern, add_unique_param, new_content, flags=re.DOTALL)

    with open(file_path, 'w') as f:
        f.write(new_content)


def generate_sqla():
    """
    Generates SQLAlchemy models from LinkML schema modules.
    """
    base_dir = Path(__file__).parent.parent
    linkml_dir = base_dir / "ca_biositing/datamodels/linkml"
    output_dir = base_dir / "ca_biositing/datamodels/schemas/generated"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Clean output directory recursively
    print(f"Cleaning output directory: {output_dir}")
    for f in output_dir.glob('**/*.py'):
        if f.name != '__init__.py':
            f.unlink()

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
