# ETL Pipeline Project

This project implements a modular ETL (Extract, Transform, Load) pipeline that
extracts data from Google Sheets (or other sources), transforms it using Python,
and loads it into a PostgreSQL database. The entire environment is containerized
with Docker.

---

## Local Development Environment (Pixi)

This project uses **Pixi** to manage dependencies and run tasks for local
development. This environment is used for both running the application locally
and for code quality tools like `pre-commit`. The Docker container also uses
Pixi to install dependencies.

**1. Install Pixi:**

- Follow the official instructions to
  [install Pixi](https://pixi.sh/latest/installation/) on your system.

**2. Install Local Dependencies:**

- Once Pixi is installed, navigate to the `ca-biositing` root directory and run:

  ```bash
  pixi install
  ```

  This will install the required local tools (like `pre-commit`) into a managed
  environment.

  If you have issues with the install on Windows, you may need to command:

  ```
  pixi workspace platform add win-64
  ```

  Once pixi is installed, run the following command to set up pre-commit checks on every commit:

  ```bash
  pixi run pre-commit-install
  ```

**3. Activate the Local Environment:**

- To activate this environment in your shell, run:

  ```bash
  pixi shell
  ```

  This command is the equivalent of a traditional `source venv/bin/activate`.
  You will see a prefix in your shell prompt indicating that the environment is
  active. You can now run commands like `pre-commit` directly.

---

## Getting Started

Follow these steps to set up and run the project for the first time. **[SUGGESTION: CHANGE ORDER OF GETTING STARTED. At step 2 I create an environment set up .env file and it says to populate the .env file with specific database connection settings but does not explain how I get database connection settings like POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_secret_password
POSTGRES_DB=your_db_name. If its okay I don't have one of those yet, let's make the note that we wont need one of those until we execute the ETL to the db.]**

**1. Google Cloud Setup:**

- To allow the application to access Google Sheets, you must first create a
  service account and generate a `credentials.json` file.
- **[Follow the full guide here: GCP_SETUP.md](./GCP_SETUP.md)**

**2. Environment Setup:**

- Create a `.env` file in the `my_etl_project` directory by copying the
  `.env.example` file.
- Populate the `.env` file with your specific database connection settings. **[Add more instruction about where such connection specifications are found.]**

**3. Build the Docker Image:**

- Build the Docker image, which will install all application dependencies using
  Pixi. **[EXPLAIN HOW TO OPEN/ACTIVATE PIXI, OR POINT TO ABOVE INSTRUCTIONS. Do I need to make sure I am in the ca-biositing directory? Is it a problem if I run docker-compose build without activating the pixi shell?]**

  ```bash
  docker-compose build
  ```

**4. Start the Services:**

- Start the application and database containers in detached mode.

  ```bash
  docker-compose up -d
  ```

**5. Apply Database Migrations:**

- The first time you start the project, you need to apply the database
  migrations to create the tables.

  ```bash
  docker-compose exec app alembic upgrade head
  ```

**[Do I need Alembic set up before this? Should there be a direction towards the alembic workflow before this point or does alembic workflow guide only needed for when youre running the ETL? I think it would be good to clarify that here.]**
The environment is now fully set up and running.

---

## Core Workflows

This project has three key development workflows. The README provides a
high-level overview, but for detailed, step-by-step instructions, please refer
to the dedicated workflow guides. **[I like this high level overview for conceptual understanding, and think it might be good to move it up so that the Getting Started steps make more sense. Otherwise, maybe adding another section that's a even broader explanation of all the components you'll need for set up might be good ("Here are the 7 installations you'll need across 4 core worfklows."; "Here is a graphical breakdown of how the ETL tools work together"). Only after I read this Core Workflows section did some of my confusions from the Getting Started section reduce, which makes me think some of this high level understanding of the workflows would help coming in earlier. ]**

### 1. Docker Environment Management

- **Purpose:** Managing the lifecycle of your development containers (app and
  database).
- **Details:** For starting, stopping, and rebuilding your environment.
- **[See the full guide: DOCKER_WORKFLOW.md](./DOCKER_WORKFLOW.md)**

### 2. Database Schema Migrations (Alembic)

- **Purpose:** Making and applying changes to the database schema (e.g., adding
  tables or columns).
- **Details:** How to automatically generate and apply migration scripts based
  on your SQLModel changes.
- **[See the full guide: ALEMBIC_WORKFLOW.md](./ALEMBIC_WORKFLOW.md)**

### 3. ETL Pipeline Development (Prefect)

- **Purpose:** Running the ETL pipeline and adding new data pipelines using
  Prefect's "flow of flows" pattern.
- **Details:** The `run_prefect_flow.py` script acts as a master orchestrator
  that runs all individual pipeline flows defined in the `src/flows/` directory.
  To add a new pipeline, you must create a new flow file and add it to the
  master flow.
- **[See the full guide: ETL_WORKFLOW.md](./ETL_WORKFLOW.md)**

### 4. Creating New Database Models

- **Purpose:** Adding a new table to the database schema.
- **Details:** Use the `model_template.py` to define your new table, then follow
  the Alembic workflow to generate and apply the migration.
- **[See the model template: src/models/templates/model_template.py](./src/models/templates/model_template.py)**
- **[See the migration guide: ALEMBIC_WORKFLOW.md](./ALEMBIC_WORKFLOW.md)**

---

## Project Structure

Here is a brief overview of the key directories in this project:

**[Edit to reflect/explain details relevant to the fact we are now working in a folder in a larger directory.]**

```
my_etl_project/
├── alembic/               # Database migration scripts
├── src/
│   ├── etl/
│   │   ├── extract/       # ETL Task: Modules for extracting data
│   │   ├── transform/     # ETL Task: Modules for transforming data
│   │   ├── load/          # ETL Task: Modules for loading data
│   │   └── templates/     # Templates for new ETL modules
│   ├── flows/             # Prefect Flows: Individual pipeline definitions
│   ├── models/            # SQLModel class definitions (database tables)
│   └── utils/             # Shared utility functions
├── .env                   # Local environment variables (you must create this)
├── docker-compose.yml     # Defines the project's services (app, db)
├── Dockerfile             # Instructions for building the app container
└── run_prefect_flow.py    # The master script to execute all ETL flows
```
