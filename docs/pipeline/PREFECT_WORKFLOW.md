# Prefect Workflow for BioCirV ETL

This document outlines the steps to start, run, and monitor the ETL pipeline
using Prefect and Docker.

## 1. Start the Prefect Environment

All services (Postgres database, Prefect server, and Prefect worker) are managed
via Docker Compose through Pixi tasks.

To start all services in detached mode:

```bash
pixi run start-services
```

This command will:

- Build the Docker images if they don't exist.
- Start the containers for the database, the Prefect server, and the Prefect
  worker.
- The Prefect worker will automatically connect to the server and its work pool.

You can check the status of the containers with `pixi run service-status`.

## 2. Deploy the ETL Flow(s)

Before you can run the pipeline, you need to deploy your flow(s) to the Prefect
server. This registers the flow and makes it available to be run by a worker.

To deploy the flow(s):

```bash
pixi run deploy
```

This command uses the configuration defined in `resources/prefect/prefect.yaml`.

## 3. Run the ETL Pipeline

Once the environment is running and the flow is deployed, you can trigger a
pipeline run.

### Running the Master Pipeline

To run the entire ETL process, which orchestrates all the sub-flows:

```bash
pixi run run-etl
```

This command instructs the Prefect server to create a new flow run for the
master deployment. The Prefect worker will pick up this run and execute the
entire pipeline.

## 4. Monitor the Pipeline

You can monitor the progress and view the logs of your pipeline runs in
real-time through the Prefect UI.

- **Prefect UI URL**: [http://localhost:4200](http://localhost:4200)

From the UI, you can see:

- The status of each task (running, completed, failed).
- Detailed logs for each task.
- A history of all flow runs.

## 5. Stopping the Environment

To stop all running Docker containers:

```bash
pixi run teardown-services
```

If you also want to remove the PostgreSQL data volume (deletes all data):

```bash
pixi run teardown-services-volumes
```
