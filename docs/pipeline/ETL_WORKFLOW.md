# ETL Pipeline Workflow

This guide explains the structure of the ETL (Extract, Transform, Load) pipeline
and how to use Prefect to execute it.

---

### Core Concepts

The ETL pipeline extracts data from Google Sheets, transforms it using pandas,
and loads it into the PostgreSQL database.

- **Structure:** The core logic is organized into three main packages within
  `src/ca_biositing/pipeline/ca_biositing/pipeline/etl/`:
  - `extract`: Functions to pull raw data from sources (e.g., Google Sheets).
  - `transform`: Functions to clean, process, and structure the raw data.
  - `load`: Functions to insert the transformed data into the database using
    SQLAlchemy.

- **Hierarchical Pipelines:** Individual pipelines are nested within
  subdirectories reflecting the data they handle (e.g., `products`, `biomass`).

---

### Running the ETL Pipelines

The ETL system runs in a containerized Prefect environment.

**Step 1: Start Services**

```bash
pixi run start-services
```

**Step 2: Deploy Flows**

```bash
pixi run deploy
```

**Step 3: Run the Master Pipeline**

```bash
pixi run run-etl
```

**Step 4: Monitor** Access the Prefect UI at
[http://localhost:4200](http://localhost:4200).

---

### How to Add a New ETL Flow

**Step 1: Create the Task Files** Create the three Python files for your
extract, transform, and load logic in the appropriate subdirectories under
`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/`. Decorate each function
with `@task`.

**Step 2: Create the Pipeline Flow** Create a new file in
`src/ca_biositing/pipeline/ca_biositing/pipeline/flows/` to define the flow.

```python
from prefect import flow
from ca_biositing.pipeline.etl.extract.samples.new_type import extract
from ca_biositing.pipeline.etl.transform.samples.new_type import transform
from ca_biositing.pipeline.etl.load.samples.new_type import load

@flow
def new_type_flow():
    raw_data = extract()
    transformed_data = transform(raw_data)
    load(transformed_data)
```

**Step 3: Register the New Flow** Add your flow to the `AVAILABLE_FLOWS`
dictionary in `resources/prefect/run_prefect_flow.py`.

**Step 4: Deploy and Run**

```bash
pixi run deploy
pixi run run-etl
```

---

### Using Templates

Template files are available in
`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/templates/` to help you get
started with new tasks.
