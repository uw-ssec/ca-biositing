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

    # 4. Generate migration
    print(f"--- Generating migration: {args.message} ---")

    # Construct the bash command to run inside the container
    # usage of shlex.quote ensures the message is safely quoted for the inner bash shell
    safe_message = shlex.quote(args.message)
    inner_cmd = f"source /shell-hook.sh && alembic revision --autogenerate -m {safe_message}"

    # We invoke docker-compose directly via pixi to avoid potential argument parsing issues
    # with pixi task aliases when handling complex nested quotes.
    cmd = [
        "pixi", "run", "docker-compose",
        "-f", "resources/docker/docker-compose.yml",
        "exec", "prefect-worker",
        "/bin/bash", "-c", inner_cmd
    ]
    run_command(cmd)

    print("--- Schema update orchestration complete! ---")
    print("Don't forget to run 'pixi run migrate' to apply the changes.")

if __name__ == "__main__":
    main()
