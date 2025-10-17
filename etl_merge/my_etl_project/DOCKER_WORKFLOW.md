# Docker Development Workflow

This guide provides a quick reference for the common Docker commands and
workflows used in this project.

---

### Production Docker Workflow

This is the standard process for running the full, containerized ETL system,
including the Prefect worker.

**1. Starting Your Environment:**

To start all services (`db`, `app`, and `prefect-worker`) and run them in the
background, use:

```bash
# Make sure you are in the my_etl_project directory
docker-compose up -d
```

This command will:

- Start the PostgreSQL database.
- Start the main application container.
- Start a dedicated Prefect worker container that automatically connects to your
  Prefect server.

**2. Stopping Your Environment:**

To stop and remove all running containers, use:

```bash
# Make sure you are in the my_etl_project directory
docker-compose down
```

---

### How to Add a New Python Package

This is the process to follow whenever you need to add a new dependency (e.g.,
`a-new-package`) to your project using Pixi.

**Step 1: Add the Dependency with Pixi**

From the project root (`ca-biositing`), use the `pixi add` command. This will
automatically update your `pixi.toml` and `pixi.lock` files.

```bash
# Make sure you are in the ca-biositing directory
pixi add a-new-package
```

**Step 2: Rebuild Your Docker Images**

Because you've changed the project's dependencies, you must rebuild your Docker
images to include the new package.

```bash
# Make sure you are in the my_etl_project directory
docker-compose up --build -d
```

Your `app` and `prefect-worker` containers will now have the new package
installed and ready to use.
