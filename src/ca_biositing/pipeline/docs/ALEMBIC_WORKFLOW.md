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

### Generating an Initial Migration

If you need to generate a completely new initial migration (e.g., starting fresh
or after major model changes), follow this procedure using the `setup-db` service:

**Step 1: Reset the Environment**

Completely tear down services and remove all data:

```bash
pixi run teardown-services-volumes
```

**Step 2: Remove Old Migration Files**

Clear the existing migration history:

```bash
rm alembic/versions/*.py
```

**Step 3: Generate the Initial Migration**

Use the `setup-db` service to generate the migration. This service has the
proper environment and file access needed for Alembic:

```bash
docker-compose -f resources/docker/docker-compose.yml run --rm setup-db alembic revision --autogenerate -m "Initial migration"
```

**Note:** The `setup-db` service is specifically designed for database
initialization and migrations. It has access to all model files and the
correct Python path configuration.

**Step 4: Apply the Migration**

Start the services. The `setup-db` service will automatically apply the newly
created migration upon startup:

```bash
pixi run start-services
```

The database schema is now initialized with your current models.

---

### The Migration Workflow

This is the standard process to follow whenever you make a change to your
database models (the files in `ca_biositing/datamodels/`).

**Important:** All Alembic commands should be run using the `setup-db` service
to ensure they have access to the database and the correct Python environment.

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
docker-compose -f resources/docker/docker-compose.yml run --rm setup-db alembic revision --autogenerate -m "A descriptive message about your changes"
```

- `docker-compose ... run --rm setup-db`: Executes the command inside the
  `setup-db` service which has proper access to model files and database
- `--rm`: Removes the container after the command completes
- `-m "..."`: A required message describing what the migration does (e.g., "Add
  user_email column to users table")

**Step 3: Apply the Migration**

After the migration script is generated, you need to apply it to the database.
The easiest way is to restart services, which will automatically apply migrations:

```bash
pixi run teardown-services
pixi run start-services
```

Alternatively, you can manually apply migrations:

```bash
docker-compose -f resources/docker/docker-compose.yml run --rm setup-db alembic upgrade head
```

- `alembic upgrade head`: Applies all migrations up to the latest version
  (`head`)

Your database schema now matches your SQLModel definitions. You can verify the
changes by connecting to the database or by inspecting the `alembic_version`
table, which tracks the applied migrations.

---

### Collaborative Workflows and Resetting the Database

When working in a team, you may pull new migration files from your colleagues.
The standard workflow is to run `alembic upgrade head` after pulling the latest
code.

However, if you have created a local migration _before_ pulling, you may run
into a "multiple heads" conflict. While there are advanced ways to fix this, the
simplest and most reliable solution for a local development environment is to
reset the database.

**The `reset_db.sh` Script**

A script named `reset_db.sh` is included in this directory to automate the
process. It provides a one-command solution to wipe the database and rebuild it
from the latest migration history.

**When to Use It:**

- When you encounter a "multiple heads" error.
- When your database gets into an inconsistent state.
- Any time you want a fresh, clean slate for testing.

**How to Use It:** From the project root directory (`ca-biositing`), run:

```bash
./src/pipeline/utils/reset_db.sh
```

This command will stop the containers, remove the database volume, restart the
containers, and apply all migrations, guaranteeing a clean and correct schema.

### How to Downgrade a Migration (Optional)

If you need to undo a migration, you can downgrade it.

```bash
# Downgrade by one version
docker-compose -f resources/docker/docker-compose.yml run --rm setup-db alembic downgrade -1

# Downgrade to a specific version
docker-compose -f resources/docker/docker-compose.yml run --rm setup-db alembic downgrade <version_number>
```
