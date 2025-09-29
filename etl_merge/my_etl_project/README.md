# ETL Pipeline Project

This project implements a modular ETL (Extract, Transform, Load) pipeline that extracts data from Google Sheets (or other sources), transforms it using Python, and loads it into a PostgreSQL database. The entire environment is containerized with Docker.

---

## Getting Started

Follow these steps to set up and run the project for the first time.

**1. Google Cloud Setup:**

*   To allow the application to access Google Sheets, you must first create a service account and generate a `credentials.json` file.
*   **[Follow the full guide here: GCP_SETUP.md](./GCP_SETUP.md)**

**2. Environment Setup:**

*   Create a `.env` file in the `my_etl_project` directory by copying the `.env.example` file.
*   Populate the `.env` file with your specific database connection settings.

**3. Install Dependencies & Build Image:**

*   This project uses Docker, so you do not need to install Python packages locally. The dependencies are managed in `requirements.txt`.
*   Build the Docker image, which will install all required packages.

    ```bash
    docker-compose build
    ```

**4. Start the Services:**

*   Start the application and database containers in detached mode.

    ```bash
    docker-compose up -d
    ```

**5. Apply Database Migrations:**

*   The first time you start the project, you need to apply the database migrations to create the tables.

    ```bash
    docker-compose exec app alembic upgrade head
    ```

The environment is now fully set up and running.

---

## Core Workflows

This project has three key development workflows. The README provides a high-level overview, but for detailed, step-by-step instructions, please refer to the dedicated workflow guides.

### 1. Docker Environment Management

*   **Purpose:** Managing the lifecycle of your development containers (app and database).
*   **Details:** For starting, stopping, and rebuilding your environment.
*   **[See the full guide: DOCKER_WORKFLOW.md](./DOCKER_WORKFLOW.md)**

### 2. Database Schema Migrations (Alembic)

*   **Purpose:** Making and applying changes to the database schema (e.g., adding tables or columns).
*   **Details:** How to automatically generate and apply migration scripts based on your SQLModel changes.
*   **[See the full guide: ALEMBIC_WORKFLOW.md](./ALEMBIC_WORKFLOW.md)**

### 3. ETL Pipeline Development

*   **Purpose:** Running the ETL pipeline and adding new data pipelines.
*   **Details:** How to execute the main pipeline script and how to use the provided templates to create new ETL modules.
*   **[See the full guide: ETL_WORKFLOW.md](./ETL_WORKFLOW.md)**

### 4. Creating New Database Models

*   **Purpose:** Adding a new table to the database schema.
*   **Details:** Use the `model_template.py` to define your new table, then follow the Alembic workflow to generate and apply the migration.
*   **[See the model template: src/models/templates/model_template.py](./src/models/templates/model_template.py)**
*   **[See the migration guide: ALEMBIC_WORKFLOW.md](./ALEMBIC_WORKFLOW.md)**

---

## Project Structure

Here is a brief overview of the key directories in this project:

```
my_etl_project/
├── alembic/               # Database migration scripts
├── src/
│   ├── etl/
│   │   ├── extract/       # Modules for extracting data
│   │   ├── transform/     # Modules for transforming data
│   │   ├── load/          # Modules for loading data
│   │   └── templates/     # Templates for new ETL modules
│   ├── models/            # SQLModel class definitions (database tables)
│   └── utils/             # Shared utility functions
├── .env                   # Local environment variables (you must create this)
├── docker-compose.yml     # Defines the project's services (app, db)
├── Dockerfile             # Instructions for building the app container
└── run_pipeline.py        # The main script to execute the ETL pipeline
