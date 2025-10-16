# ETL Pipeline Workflow

This guide explains the structure of the ETL (Extract, Transform, Load) pipeline
and how to use Prefect to execute it.

---

### Core Concepts

The ETL pipeline is designed to extract data from Google Sheets, transform it
into a structured format, and load it into the PostgreSQL database. The system
is built to be modular and extensible.

- **Structure:** The core logic is organized into three main packages within
  `src/etl/`:

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

### Development Workflow: Ad-Hoc Runs

For quick, script-based execution, you can use `run_prefect_flow.py` directly.
This is ideal for simple debugging or manual runs.

#### Running the Master Flow

To run all ETL pipelines, execute the script without arguments:

```bash
pixi run python run_prefect_flow.py
```

#### Running a Specific Flow

To run one or more specific flows, pass their names as arguments:

```bash
# Run only the primary_product flow
pixi run python run_prefect_flow.py primary_product

# Run both the primary_product and analysis_type flows
pixi run python run_prefect_flow.py primary_product analysis_type
```

---

### Production Workflow: Using the Prefect Server and Docker

For a robust, observable, and containerized experience, use the Prefect server
in combination with the Docker environment.

> **Note on Directories:** All `docker-compose` and `pixi` commands in this
> section should be run from the `my_etl_project` directory. From the project
> root, you can navigate there with: `cd etl_merge/my_etl_project`

**Step 1: Start the Prefect Server**

In one terminal, start the Prefect UI and server on your **host machine**. This
process runs in the background.

```bash
pixi run prefect server start
```

You can access the dashboard at [http://127.0.0.1:4200](http://127.0.0.1:4200).

**Step 2: Start the Docker Environment**

In a **new terminal**, start the full Docker environment. This will start the
database, the main app, and the containerized Prefect worker.

```bash
docker-compose up -d
```

The `prefect-worker` service is configured to automatically connect to the
Prefect server running on your host.

**Step 3: Deploy and Run a Flow**

Deployments make your flows available to the Prefect server.

1.  **Deploy the Flow (First time only):** The first time you create or update a
    flow, you must deploy it from your **host machine**. This command creates a
    `prefect.yaml` file that saves your deployment settings.

    ```bash
    pixi run prefect deploy run_prefect_flow.py:master_flow
    ```

2.  **Trigger a Flow Run:** To run a deployed flow, use the
    `prefect deployment run` command from your **host machine**. The
    containerized worker will automatically pick up and execute the run.

    ```bash
    pixi run prefect deployment run 'Master ETL Flow/biocirv_master_flow_test_deploy'
    ```

You can now monitor the run in real-time in the Prefect UI.

---

### How to Add a New ETL Flow

To add a new pipeline (e.g., for "new_sample_type"), you must create the
necessary task files, define a new flow for that pipeline, and then register it
in the main `run_prefect_flow.py` script.

**Step 1: Create the Task Files**

Create the three Python files for your extract, transform, and load logic in the
appropriate subdirectories. Decorate each function with `@task`.

- `src/etl/extract/samples/new_sample_type.py`
- `src/etl/transform/samples/new_sample_type.py`
- `src/etl/load/samples/new_sample_type.py`

**Step 2: Create the Pipeline Flow**

Create a new file in the `src/flows/` directory to define the flow for your new
pipeline. For example: `src/flows/new_sample_type.py`.

Inside this file, import your tasks and define a flow function that orchestrates
them:

```python
# src/flows/new_sample_type.py
from prefect import flow
from src.etl.extract.samples.new_sample_type import extract
from src.etl.transform.samples.new_sample_type import transform
from src.etl.load.samples.new_sample_type import load

@flow
def new_sample_type_flow():
    raw_data = extract()
    transformed_data = transform(raw_data)
    load(transformed_data)
```

**Step 3: Register the New Flow**

Finally, open `run_prefect_flow.py` to make the new flow available to the
runner. This is a **manual step** that ensures only explicitly registered flows
are run.

1.  **Import your new flow function** at the top of the script:
    ```python
    from src.flows.new_sample_type import new_sample_type_flow
    ```
2.  **Add the flow to the `AVAILABLE_FLOWS` dictionary**. This makes it runnable
    from the command line and includes it in the master flow.
    ```python
    AVAILABLE_FLOWS = {
        "primary_product": primary_product_flow,
        "analysis_type": analysis_type_flow,
        "new_sample_type": new_sample_type_flow,  # Add your new flow here
    }
    ```

**Step 4: Run the Master Flow**

The next time you run `python run_prefect_flow.py`, your new pipeline will be
executed as part of the master flow.

---

### How to Add a New ETL Flow Using Templates

The process is the same as above, but you start by copying the templates.

**Step 1: Copy and Customize the Template Files**

Copy the templates from `src/etl/templates/` to your new module directories and
customize the `TODO` sections. The templates already include the `@task`
decorator.

**Step 2: Create the Pipeline Flow**

Create a new flow file in `src/flows/` that imports and orchestrates your new
tasks.

**Step 3: Register the New Flow**

Open `run_prefect_flow.py`, import your new flow, and add it to the
`AVAILABLE_FLOWS` dictionary.
