import os
import re
from pathlib import Path
from collections import deque

def sort_sql_files():
    base_path = Path("src/ca_biositing/datamodels/ca_biositing/datamodels/sql_schemas")
    tables_path = base_path / "tables"

    # 1. Map files to table names and extract dependencies
    table_to_file = {}
    dependencies = {} # table -> set of tables it depends on

    # Regex to find table name in file
    table_regex = re.compile(r"CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS\s+(\w+)", re.IGNORECASE)
    # Regex to find foreign key references
    ref_regex = re.compile(r"REFERENCES\s+(\w+)\s*\(", re.IGNORECASE)

    all_table_files = list(tables_path.glob("*.sql"))

    for file_path in all_table_files:
        content = file_path.read_text()

        table_match = table_regex.search(content)
        if not table_match:
            continue

        table_name = table_match.group(1).lower()
        table_to_file[table_name] = f"tables/{file_path.name}"

        # Extract dependencies
        refs = set(ref_regex.findall(content))
        # Remove self-references and non-existing tables (system or other schemas)
        refs = {ref.lower() for ref in refs if ref.lower() != table_name}
        dependencies[table_name] = refs

    # 2. Topological Sort (Kahn's Algorithm)
    sorted_tables = []

    # Track in-degrees (number of tables that depend on a table)
    # Actually, we need the reverse for Kahn's: tables that this table depends on
    # Let's use a simpler DFS-based topological sort

    visited = set()
    temp_visited = set()

    def visit(node):
        if node in temp_visited:
            # Cycle detected (e.g. self-reference or mutual FK)
            # In Postgres these are possible, we'll just break the cycle by ignoring the dependency
            return
        if node in visited:
            return

        temp_visited.add(node)

        # Visit dependencies that are in our set of tracked tables
        for dep in dependencies.get(node, []):
            if dep in table_to_file:
                visit(dep)

        temp_visited.remove(node)
        visited.add(node)
        sorted_tables.append(node)

    for table in table_to_file:
        if table not in visited:
            visit(table)

    # 3. Handle non-table files (Types, Views, Privileges)
    types = [f"types/{f.name}" for f in (base_path / "types").glob("*.sql")]
    views = [f"views/{f.name}" for f in (base_path / "views").glob("*.sql")]
    privileges = [f"privileges/{f.name}" for f in (base_path / "privileges").glob("*.sql")]

    # 4. Generate main.sql
    with open(base_path / "main.sql", "w") as f:
        f.write("--\n-- pgschema database dump (Automated Topological Sort)\n--\n\n")

        f.write("-- Extensions & Types\n")
        for t in sorted(types):
            f.write(f"\\i {t}\n")
        f.write("\n")

        f.write("-- Tables (Dependency Sorted)\n")
        for table in sorted_tables:
            f.write(f"\\i {table_to_file[table]}\n")
        f.write("\n")

        f.write("-- Views\n")
        for v in sorted(views):
            f.write(f"\\i {v}\n")
        f.write("\n")

        f.write("-- Privileges\n")
        for p in sorted(privileges):
            f.write(f"\\i {p}\n")

    print(f"Successfully reordered {len(sorted_tables)} tables in main.sql")

if __name__ == "__main__":
    sort_sql_files()
