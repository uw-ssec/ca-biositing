import subprocess
import sys
import argparse
import shlex
from pathlib import Path

def run_command(command, cwd=None):
    print(f"Running: {command}")
    try:
        # If command is a string, use shell=True. If list, use shell=False.
        shell = isinstance(command, str)
        subprocess.run(command, shell=shell, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        sys.exit(e.returncode)

def main():
    parser = argparse.ArgumentParser(description="Orchestrate schema update workflow.")
    parser.add_argument("-m", "--message", required=True, help="Migration message")
    args = parser.parse_args()

    # 1. Generate SQLAlchemy models
    print("--- Generating SQLAlchemy models ---")
    script_path = Path(__file__).parent / "generate_sqla.py"
    run_command(f"python {script_path}")

    # 2. Rebuild services
    print("--- Rebuilding services ---")
    # We assume we are in the project root or pixi handles the path
    run_command("pixi run rebuild-services")

    # 3. Start services
    print("--- Starting services ---")
    run_command("pixi run start-services")

    # Add a short pause and retry loop to ensure the database container is ready
    import time, subprocess
    max_retries = 12  # total ~60 seconds
    for attempt in range(1, max_retries + 1):
        print(f"--- Checking database health (attempt {attempt}/{max_retries}) ---")
        try:
            subprocess.run(["pixi", "run", "check-db-health"], check=True)
            print("Database is healthy.")
            break
        except subprocess.CalledProcessError:
            if attempt == max_retries:
                print("Database health check failed after maximum retries. Exiting.")
                sys.exit(1)
            time.sleep(5)

    # 5. Generate migration (Locally to avoid container import hangs)
    print(f"--- Generating migration locally: {args.message} ---")

    import os
    # Prepare environment for local alembic run
    # NOTE: Packages are installed in the pixi environment, so PYTHONPATH
    # manipulation is not needed. The packages (ca-biositing-datamodels,
    # ca-biositing-pipeline, ca-biositing-webservice) are properly discoverable
    # through the virtual environment managed by pixi.
    local_env = os.environ.copy()

    # Point to the Docker database via localhost
    # We assume the user has the default port 5432 mapped as per docker-compose.yml
    if not local_env.get("DATABASE_URL"):
        local_env["DATABASE_URL"] = "postgresql://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db"

    local_env["EDITOR"] = "true"

    # Find project root for cwd
    # Script is at: resources/linkml/scripts/orchestrate_schema_update.py
    # 4 levels up to reach project root: scripts/ -> linkml/ -> resources/ -> project root
    project_root = Path(__file__).resolve().parent.parent.parent.parent

    cmd = [
        "pixi", "run", "alembic",
        "-c", "alembic.ini",
        "revision", "--autogenerate",
        "-m", args.message
    ]

    print(f"Running local migration generation in {project_root} via pixi environment...")
    try:
        subprocess.run(cmd, env=local_env, check=True, cwd=str(project_root))
    except subprocess.CalledProcessError as e:
        print(f"Error running local alembic: {e}")
        sys.exit(e.returncode)

    print("--- Schema update orchestration complete! ---")
    print("Don't forget to run 'pixi run migrate' to apply the changes.")

if __name__ == "__main__":
    main()
