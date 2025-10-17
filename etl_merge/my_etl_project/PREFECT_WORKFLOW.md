# Prefect Workflow for BioCirV ETL

This document outlines the steps to start, run, and monitor the ETL pipeline
using Prefect and Docker.

## Prerequisites

- Docker and Docker Compose must be installed and running on your system.

## 1. Start the Prefect Environment

All services (Postgres database, Prefect server, Prefect worker, and the
application environment) are managed via Docker Compose.

To start all services in detached mode, navigate to the `my_etl_project`
directory and run:

```bash
cd etl_merge/my_etl_project
docker-compose up -d
```

This command will:

- Build the Docker images if they don't exist.
- Start the containers for the database, the Prefect server, the Prefect worker,
  and the main application.
- The Prefect worker will automatically connect to the server and its work pool.

You can check the status of the containers with `docker-compose ps`.

## 2. Deploy the ETL Flow(s)

Before you can run the pipeline, you need to deploy your flow(s) to the Prefect
server. This registers the flow and makes it available to be run by a worker.

To deploy the flow(s), run the following command from the `my_etl_project`
directory:

```bash
docker-compose exec app pixi run prefect deploy
```

### A Note on First-Time Deployment

The first time you run `prefect deploy`, it will be an interactive process where
you confirm the flow to deploy. This action creates the `prefect.yaml` file,
which stores your deployment configurations.

After choosing a deployment, answering no the following questions is encouraged
if seeking easy deployment.

**This is a one-time setup.** For any subsequent user, or for any future
deployments, running `prefect deploy` will be non-interactive and will simply
apply the configurations defined in `prefect.yaml`.

## 3. Run the ETL Pipeline

Once the environment is running and the flow is deployed, you can trigger a
pipeline run.

### Running the Master Pipeline

To run the entire ETL process, which orchestrates all the sub-flows, use the
following command:

```bash
docker-compose exec app pixi run prefect deployment run 'Master ETL Flow/master-etl-deployment'
```

This command instructs the Prefect server to create a new flow run for the
master deployment. The Prefect worker will pick up this run and execute the
entire pipeline.

### Running Individual Pipelines

To run a sub-pipeline individually (e.g., only the `primary_product` ETL), you
first need to define a deployment for it in your `prefect.yaml` file.

For example, to create a deployment for the `primary_product_flow`, you would
add the following to the `deployments` section of `prefect.yaml`:

```yaml
# prefect.yaml

deployments:
  - name: master-etl-deployment
    # ... (existing configuration) ...

  - name: primary-product-deployment
    version: 1.0
    tags: ["etl", "product"]
    description: A flow for the primary product ETL pipeline.
    entrypoint: src/flows/primary_product.py:primary_product_flow
    work_pool:
      name: biocirv_dev_work_pool
```

After adding this configuration, run `prefect deploy` again to register it:

```bash
docker-compose exec app pixi run prefect deploy
```

Then, you can run just that pipeline with its specific command:

```bash
docker-compose exec app pixi run prefect deployment run 'Primary Product ETL/primary-product-deployment'
```

## 4. Monitor the Pipeline

You can monitor the progress and view the logs of your pipeline runs in
real-time through the Prefect UI.

- **Prefect UI URL**: [http://localhost:4200](http://localhost:4200)

From the UI, you can see:

- The DAG (Directed Acyclic Graph) of your flow.
- The status of each task (running, completed, failed).
- Detailed logs for each task.
- A history of all flow runs.

## 5. Stopping the Environment

To stop all running Docker containers, use the following command:

```bash
docker-compose down
```

If you also want to remove the PostgreSQL data volume, you can add the `-v`
flag:

```bash
docker-compose down -v
```
