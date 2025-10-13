# Alembic Database Migration Workflow

This guide provides a reference for using Alembic to manage your database
schema. Alembic allows you to make changes to your database structure in a
systematic and version-controlled way.

---

### Core Concepts

- **What is Alembic?** Alembic is a database migration tool for Python. It
  allows you to modify your database schema (e.g., add a new table or column)
  and keep a versioned history of those changes.
- **Why use it?** It prevents you from having to manually write SQL
  `ALTER TABLE` statements. It automatically compares your SQLModel classes to
  the current state of the database and generates the necessary migration
  scripts.

---

### The Migration Workflow

This is the standard process to follow whenever you make a change to your
database models (the files in `src/models/`).

**Important:** All Alembic commands must be run _inside_ the `app` container to
ensure they have access to the database and the correct Python environment.

**Step 1: Modify Your SQLModel Classes**

Make any desired changes to your models. This can be adding a new column to an
existing model or creating a completely new model file.

**Important:** If you create a **new model file** (e.g.,
`src/models/new_model.py`), you must import it in `alembic/env.py` so that
Alembic can see it. Add a line like this to the import section of `env.py`:

```python
from src.models.new_model import *
```

**Step 2: Generate a New Migration Script**

After saving your model changes, run the following command. This tells Alembic
to inspect your models, compare them to the database schema, and generate a new
migration script in the `alembic/versions` directory.

```bash
docker exec -it my_etl_project_app alembic revision --autogenerate -m "A descriptive message about your changes"
```

- `docker exec -it my_etl_project_app`: Executes the command inside the `app`
  container.
- `alembic revision --autogenerate`: Tells Alembic to create a new revision file
  based on model changes.
- `-m "..."`: A required message describing what the migration does (e.g., "Add
  user_email column to users table").

**Step 3: Apply the Migration**

After the migration script is generated, you need to apply it to the database.
This is the step that actually runs the `ALTER TABLE` commands and changes the
database schema.

```bash
docker exec -it my_etl_project_app alembic upgrade head
```

- `alembic upgrade head`: Applies all migrations up to the latest version
  (`head`).

Your database schema now matches your SQLModel definitions. You can verify the
changes by connecting to the database or by inspecting the `alembic_version`
table, which tracks the applied migrations.

### How to Downgrade a Migration (Optional)

If you need to undo a migration, you can downgrade it.

```bash
# Downgrade by one version
docker exec -it my_etl_project_app alembic downgrade -1

# Downgrade to a specific version
docker exec -it my_etl_project_app alembic downgrade <version_number>
```
