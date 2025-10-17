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

### Running the ETL Pipelines

The method for running the ETL pipelines has been updated to use a fully
containerized Prefect environment. The old methods of running flows via
`run_prefect_flow.py` or a local Prefect server are now deprecated.

For complete, up-to-date instructions on how to start the environment, deploy
flows, and run the pipelines, please refer to the new official workflow
document:

### [**`PREFECT_WORKFLOW.md`**](./PREFECT_WORKFLOW.md)

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

**Step 4: Deploy and Run the Flow**

Since you have modified the `master_flow` by adding a new sub-flow, you must
update the deployment on the Prefect server.

1.  **Update the Deployment:** Run the `deploy` command. Prefect will
    automatically use the existing `prefect.yaml` configuration.

    ```bash
    docker-compose exec app pixi run prefect deploy
    ```

2.  **Run the Master Flow:** You can now trigger a run of the updated master
    flow.
    `bash     docker-compose exec app pixi run prefect deployment run 'Master ETL Flow/master-etl-deployment'     `
    Your new pipeline will be executed as part of the master flow.

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
