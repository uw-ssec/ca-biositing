#!/usr/bin/env python3
"""
Script to load environment variables from .env file and display PREFECT_API_URL.
"""
import argparse
import os
import subprocess
from pathlib import Path
import time

from dotenv import load_dotenv


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Load environment variables from .env file and display PREFECT_API_URL"
    )
    parser.add_argument(
        "deployment_name",
        type=str,
        help="Name of the deployment",
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        default=Path(__file__).parent / ".env",
        help="Path to the .env file (default: .env in the script's directory)",
    )
    args = parser.parse_args()
    
    # Load .env file from the specified path
    env_path = args.env_file
    
    if not env_path.exists():
        print(f"Error: .env file not found at {env_path}")
        return 1
    
    # Load environment variables from .env file
    load_dotenv(env_path)
    
    # Display deployment name
    print(f"Deployment name: {args.deployment_name}")
    
    # Get PREFECT_API_URL from environment
    prefect_api_url = os.getenv("PREFECT_API_URL")
    
    if prefect_api_url:
        print(f"PREFECT_API_URL from .env file: {prefect_api_url}")
    else:
        print("PREFECT_API_URL not found in environment variables")
    
    return_code = -1
    
    while return_code != 0:
        # Also run the shell command to echo $PREFECT_API_URL
        print("\nDeploying with Prefect...")
        result = subprocess.run(
            ["prefect", "--no-prompt", "deploy", "--name", args.deployment_name],
            shell=False,
            capture_output=True,
            text=True,
            env=os.environ.copy()
        )
        
        stdout_result = result.stdout.strip()
        return_code = result.returncode
        if return_code == 0:
            print("Deployment succeeded.")
            print(stdout_result)
            break
        else:
            print(f"Return code: {return_code}")
            print(stdout_result)
            print("Waiting for 5 seconds before retrying...")
            time.sleep(5)
    
    return 0


if __name__ == "__main__":
    exit(main())
