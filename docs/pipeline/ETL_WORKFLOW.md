# ETL Pipeline Workflow

This guide explains the structure of the ETL (Extract, Transform, Load) pipeline
and how to use Prefect to execute it.

---

### Core Concepts

The ETL pipeline is designed to extract data from Google Sheets, transform it
into a structured format, and load it into the PostgreSQL database. The system
is built to be modular and extensible.

- **Structure:** The core logic is organized into three main packages within
  `src/pipeline/etl/`:
  - `extract`: Contains functions to pull raw data from sources (e.g., Google
    Sheets).
  - `transform`: Contains functions to clean, process, and structure the raw
    data.
  - `load`: Contains functions to insert the transformed data into the database.

- **Hierarchical Pipelines:** To keep the project organized, individual
  pipelines are nested within subdirectories that reflect the data they handle
  (e.g., `products`, `analysis`). A complete pipeline for a single data type,
  like `primary_product`, consists of three corresponding files:
  - `src/etl/extract/products/primary_product.py`
  - `src/etl/transform/products/primary_product.py`
  - `src/etl/load/products/primary_product.py`

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

**Step 1: Create the Task Files**

Create the three Python files for your extract, transform, and load logic in the
appropriate subdirectories. Decorate each function with `@task`, which is a
Prefect decorator that transforms a normal Python function into a managed Task.
Applying `@task` enables Prefect to:

- Schedule and orchestrate the function as an individual Task within a flow.
- Track the Task’s execution state (pending, running, succeeded, failed).
- Automatically handle retries, timeouts, and result caching when configured.
- Collect logs and metrics for observability and debugging.

- `src/etl/extract/samples/new_sample_type.py`
- `src/etl/transform/samples/new_sample_type.py`
- `src/etl/load/samples/new_sample_type.py`

**Step 2: Create the Pipeline Flow**

Create a new file in the `src/flows/` directory to define the flow for your new
pipeline. For example: `src/flows/new_sample_type.py`.

Inside this file, import your tasks and define a flow function that orchestrates
them:

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
