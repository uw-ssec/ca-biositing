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
  `ALTER TABLE` statements. It automatically compares your SQLAlchemy classes to
  the current state of the database and generates the necessary migration
  scripts.

---

### The Orchestrated Schema Update (Recommended)

For most development tasks involving schema changes, use the orchestrated update
task. This task handles model generation from LinkML, service rebuilding, and
local migration generation in one step.

**Step 1: Modify LinkML Schema** Edit the YAML files in
`src/ca_biositing/datamodels/ca_biositing/datamodels/linkml/modules/`.

**Step 2: Run Orchestration**

```bash
pixi run update-schema -m "Description of your changes"
```

This command:

1. Generates SQLAlchemy models from LinkML.
2. Rebuilds Docker services.
3. Starts services and waits for DB health.
4. Generates an Alembic migration script **locally** to avoid Docker filesystem
   hangs.

**Step 3: Apply the Migration**

```bash
pixi run migrate
```

This applies `alembic upgrade head` locally against the Docker-hosted database.

---

### Manual Migration Workflow

If you need to perform manual Alembic operations (e.g., manual revisions or
downgrades), follow these steps.

**Important:** Run Alembic commands locally using `pixi run` to ensure the
correct environment and to avoid performance issues with Docker on macOS.

**Step 1: Generate a New Migration Script**

```bash
# Ensure services are running first
pixi run start-services

# Generate revision
PYTHONPATH=./src/ca_biositing/datamodels DATABASE_URL=postgresql://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db pixi run alembic revision --autogenerate -m "Your message"
```

**Step 2: Apply the Migration**

```bash
pixi run migrate
```

---

### Collaborative Workflows and Resetting the Database

When working in a team, you may pull new migration files. The standard workflow
is to run `pixi run migrate` after pulling the latest code.

If you encounter a "multiple heads" conflict or your database gets into an
inconsistent state, you can reset the environment.

**Resetting the Environment:**

1. Stop and wipe volumes:
   ```bash
   pixi run teardown-services-volumes
   ```
2. Start services:
   ```bash
   pixi run start-services
   ```
3. Apply all migrations:
   ```bash
   pixi run migrate
   ```

---

### How to Downgrade a Migration (Optional)

If you need to undo a migration:

```bash
# Downgrade by one version
PYTHONPATH=./src/ca_biositing/datamodels DATABASE_URL=postgresql://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db pixi run alembic downgrade -1
```
