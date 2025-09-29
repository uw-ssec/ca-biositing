# Docker Development Workflow

This guide provides a quick reference for the common Docker commands and workflows used in this project.

---

### Daily Docker Workflow

This is your day-to-day process for starting and stopping your development environment.

**1. Starting Your Environment:**

To start all the services defined in your `docker-compose.yml` file (`app` and `pg`) and run them in the background, use:

```bash
# Make sure you are in the my_etl_project directory
docker-compose up -d
```

**2. Stopping Your Environment:**

At the end of the day, to stop the containers without deleting them (the "pause button"), use:

```bash
# Make sure you are in the my_etl_project directory
docker-compose stop
```
This is fast and allows you to quickly restart your work later with `docker-compose start` or `docker-compose up -d`.

---

### How to Add a New Python Package

This is the process to follow whenever you need to add a new dependency (e.g., `a-new-package`) to your project.

**Step 1: Activate Your Local Virtual Environment**

First, make sure your local `venv` is active so you can install and test the package locally.

```bash
# If you are in the my_etl_project directory
source venv/bin/activate
```

**Step 2: Install the New Package**

Install the package using `pip`.

```bash
pip install a-new-package
```

**Step 3: Update `requirements.txt`**

This is the most critical step. After installing the new package, you need to add it to your `requirements.txt` file. It's best to add it manually to the list to keep the file clean.

Open `my_etl_project/requirements.txt` and add the name of the new package to the list.

**Step 4: Rebuild Your Docker Image**

Because you've changed the dependencies, you must rebuild your `app` image to include the new package.

```bash
# Make sure you are in the my_etl_project directory
docker-compose build
```

**Step 5: Restart Your Containers**

Finally, bring your services down and then back up to ensure the new image is used.

```bash
# Make sure you are in the my_etl_project directory
docker-compose down
docker-compose up -d
```

Your `app` container will now have the new package installed and ready to use.
