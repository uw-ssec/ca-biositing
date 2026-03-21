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

- **Hierarchical Pipelines:** Transform and load logic are organized into
  subdirectories reflecting the data they handle (e.g., `products`, `usda`,
  `analysis`).

---

### Running the ETL Pipelines

The ETL system runs in a containerized Prefect environment.

**Step 1: Start Services**

```bash
pixi run start-services
```

**Step 2: Apply Datamodel**

```bash
pixi run migrate
```

**Step 3: Deploy Flows**

```bash
pixi run deploy
```

**Step 4: Run the Master Pipeline**

```bash
pixi run run-etl
```

**Step 5: Monitor** Access the Prefect UI at
[http://localhost:4200](http://localhost:4200).

---

### How to Add a New ETL Flow

**Step 1: Create the Task Files** Create the three Python files for your
extract, transform, and load logic under
`src/ca_biositing/pipeline/ca_biositing/pipeline/etl/`. Extract tasks go
directly in `extract/`; transform and load tasks go in appropriately named
subdirectories (e.g., `transform/products/`, `load/products/`). Decorate each
function with `@task`.

**Step 2: Create the Pipeline Flow** Create a new file in
`src/ca_biositing/pipeline/ca_biositing/pipeline/flows/` to define the flow.

```python
from prefect import flow
from ca_biositing.pipeline.etl.extract.my_source import extract
from ca_biositing.pipeline.etl.transform.products.my_product import transform
from ca_biositing.pipeline.etl.load.products.my_product import load

@flow
def my_product_flow():
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
