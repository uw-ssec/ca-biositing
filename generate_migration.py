import inspect
import os
import re
import sys
from collections import defaultdict

from ca_biositing.datamodels import biomass
from ca_biositing.datamodels import data_and_references
from ca_biositing.datamodels import experiments_analysis
from ca_biositing.datamodels import external_datasets
from ca_biositing.datamodels import geographic_locations
from ca_biositing.datamodels import metadata_samples
from ca_biositing.datamodels import organizations
from ca_biositing.datamodels import people_contacts
from ca_biositing.datamodels import sample_preprocessing
from ca_biositing.datamodels import specific_aalysis_results
from ca_biositing.datamodels import user

def get_table_dependencies():
    """
    Parses the model files to build a dependency graph of the tables.
    """
    dependencies = defaultdict(list)
    models = [
        biomass, data_and_references, experiments_analysis, external_datasets,
        geographic_locations, metadata_samples, organizations, people_contacts,
        sample_preprocessing, specific_aalysis_results, user
    ]

    for model in models:
        for name, obj in inspect.getmembers(model):
            if hasattr(obj, '__tablename__'):
                source = inspect.getsource(obj)
                for fk in re.findall(r"foreign_key=\"(.*?)\.", source):
                    dependencies[obj.__tablename__].append(fk)
    return dependencies

def topological_sort(dependencies):
    """
    Performs a topological sort on the dependency graph.
    """
    sorted_tables = []
    visited = set()

    def visit(table):
        if table in visited:
            return
        visited.add(table)
        for dep in dependencies.get(table, []):
            visit(dep)
        sorted_tables.append(table)

    for table in dependencies:
        visit(table)

    # Add tables with no dependencies
    all_tables = set(dependencies.keys())
    for deps in dependencies.values():
        all_tables.update(deps)

    for table in all_tables:
        if table not in sorted_tables:
            sorted_tables.append(table)

    return sorted_tables

def get_create_table_code(table_name):
    """
    Generates the op.create_table code for a given table.
    """
    models = [
        biomass, data_and_references, experiments_analysis, external_datasets,
        geographic_locations, metadata_samples, organizations, people_contacts,
        sample_preprocessing, specific_aalysis_results, user
    ]
    for model in models:
        for name, obj in inspect.getmembers(model):
            if hasattr(obj, '__tablename__') and obj.__tablename__ == table_name:
                source = inspect.getsource(obj)
                # This is a simplified parser. A more robust solution would use AST.
                columns = []
                for line in source.split('\n'):
                    if "Field(" in line or "Column(" in line:
                        col_name_match = re.match(r'\s*(\w+):', line)
                        if col_name_match:
                            col_name = col_name_match.group(1)
                            col_type = "sa.String()" # Default
                            if "Optional[int]" in line:
                                col_type = "sa.Integer()"
                            elif "Optional[Decimal]" in line:
                                col_type = "sa.Numeric()"
                            elif "Optional[datetime]" in line:
                                col_type = "sa.DateTime()"
                            elif "Optional[date]" in line:
                                col_type = "sa.Date()"
                            elif "Optional[bool]" in line:
                                col_type = "sa.Boolean()"
                            elif "Optional[float]" in line:
                                col_type = "sa.Float()"

                            nullable = "nullable=True" if "Optional" in line else "nullable=False"
                            primary_key = "primary_key=True" if "primary_key=True" in line else ""
                            unique = "unique=True" if "unique=True" in line else ""
                            foreign_key = ""
                            fk_match = re.search(r"foreign_key=\"(.*?)\"", line)
                            if fk_match:
                                fk_parts = fk_match.group(1).split('.')
                                foreign_key = f"sa.ForeignKeyConstraint(['{col_name}'], ['{fk_parts[0]}.{fk_parts[1]}'], )"

                            column_args = [f"'{col_name}'", col_type]
                            if not "Optional" in line:
                                column_args.append("nullable=False")
                            if primary_key:
                                column_args.append(primary_key)
                            if unique:
                                column_args.append(unique)

                            columns.append(f"    sa.Column({', '.join(column_args)})")
                            if foreign_key:
                                columns.append(f"    {foreign_key}")


                pk_columns = []
                for line in source.split('\n'):
                    if "primary_key=True" in line:
                        pk_col_match = re.match(r'\s*(\w+):', line)
                        if pk_col_match:
                            pk_columns.append(f"'{pk_col_match.group(1)}'")

                pk_constraint = ""
                if pk_columns:
                    pk_constraint = f"    sa.PrimaryKeyConstraint({', '.join(pk_columns)})"


                return f"    op.create_table('{table_name}',\n" + ",\n".join(columns) + (",\n" + pk_constraint if pk_constraint else "") + "\n    )"
    return ""


if __name__ == "__main__":
    dependencies = get_table_dependencies()
    sorted_tables = topological_sort(dependencies)

    with open("src/pipeline/alembic/versions/81f96df1e929_initial_migration_from_corrected_models.py", "w") as f:
        f.write('"""Initial migration from corrected models\n\n')
        f.write('Revision ID: 81f96df1e929\n')
        f.write('Revises: \n')
        f.write('Create Date: 2025-09-19 20:49:23.494336\n\n')
        f.write('"""\n')
        f.write('from typing import Sequence, Union\n\n')
        f.write('from alembic import op\n')
        f.write('import sqlalchemy as sa\n\n\n')
        f.write('# revision identifiers, used by Alembic.\n')
        f.write("revision: str = '81f96df1e929'\n")
        f.write("down_revision: Union[str, Sequence[str], None] = None\n")
        f.write("branch_labels: Union[str, Sequence[str], None] = None\n")
        f.write("depends_on: Union[str, Sequence[str], None] = None\n\n\n")
        f.write('def upgrade() -> None:\n')
        f.write('    """Upgrade schema."""\n')
        f.write('    # ### commands auto generated by Alembic - please adjust! ###\n')
        for table in sorted_tables:
            # A simplified way to generate the create_table code
            # In a real scenario, you might need a more robust parser
            # or use a library to inspect SQLAlchemy models.
            if table != 'testusers2':
                 f.write(get_create_table_code(table) + "\n")
        f.write('    # ### end Alembic commands ###\n\n\n')
        f.write('def downgrade() -> None:\n')
        f.write('    """Downgrade schema."""\n')
        f.write('    # ### commands auto generated by Alembic - please adjust! ###\n')
        for table in reversed(sorted_tables):
            if table != 'testusers2':
                f.write(f"    op.drop_table('{table}')\n")
        f.write('    # ### end Alembic commands ###\n')
