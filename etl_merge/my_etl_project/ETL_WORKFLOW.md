# ETL Pipeline Workflow

This guide explains the structure of the ETL (Extract, Transform, Load) pipeline
and how to use the `run_pipeline.py` script to execute it.

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

### Running the Pipeline

The `run_pipeline.py` script is the entry point for executing all or part of the
ETL process. All commands should be run from the `my_etl_project` directory.

**1. Running the Full Pipeline:**

To run all ETL pipelines that the script discovers, execute the following
command. The script will automatically find all valid pipelines and run them
sequentially.

```bash
docker-compose exec app python run_pipeline.py
```

**2. Running Specific Pipelines:**

You can also run one or more specific pipelines by passing their names as
command-line arguments. The names are derived from their path within the `etl`
directory (e.g., `products/primary_product.py` becomes
`products.primary_product`).

```bash
# Run only the primary_product pipeline
docker-compose exec app python run_pipeline.py products.primary_product

# Run both the primary_product and analysis_type pipelines
docker-compose exec app python run_pipeline.py products.primary_product analysis.analysis_type
```

---

### How to Add a New ETL Pipeline

To add a new pipeline for a new data type (e.g., "new_sample_type"), follow this
pattern:

**Step 1: Create the Module Files:**

Create the three necessary Python files in the appropriate subdirectories. For
example:

- `src/etl/extract/samples/new_sample_type.py`
- `src/etl/transform/samples/new_sample_type.py`
- `src/etl/load/samples/new_sample_type.py`

**Step 2: Implement the Functions:**

In each file, implement the required function (`extract()`, `transform()`,
`load()`). Ensure they follow the same input/output pattern as the existing
pipelines.

**Step 3: Run the New Pipeline:**

The `run_pipeline.py` script will automatically discover your new
`samples.new_sample_type` pipeline. You can run it by name or as part of the
full pipeline run.

This modular structure makes it simple and efficient to extend the ETL system
with new data sources.

---

### How to Add a New ETL Pipeline Using Templates

To accelerate development and ensure consistency, you can use the templates
located in the `src/etl/templates/` directory.

**Step 1: Copy the Template Files**

Copy the three template files into the appropriate new subdirectories for your
pipeline. For example, to create a "new_sample_type" pipeline in a "samples"
category:

- Copy `src/etl/templates/extract_template.py` to
  `src/etl/extract/samples/new_sample_type.py`
- Copy `src/etl/templates/transform_template.py` to
  `src/etl/transform/samples/new_sample_type.py`
- Copy `src/etl/templates/load_template.py` to
  `src/etl/load/samples/new_sample_type.py`

**Step 2: Customize the New Files**

Open each of the new files and follow the `TODO` comments to customize the
logic:

- **In the extract file:** Update the `WORKSHEET_NAME`.
- **In the transform file:** Implement the data cleaning and structuring logic.
- **In the load file:** Import your specific SQLModel class and map the
  DataFrame columns to your model's attributes.

**Step 3: Run the New Pipeline**

Once customized, the `run_pipeline.py` script will automatically discover your
new `samples.new_sample_type` pipeline. You can run it by name or as part of the
full pipeline run.
