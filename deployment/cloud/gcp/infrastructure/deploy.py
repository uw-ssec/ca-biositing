"""Pulumi Automation API entry point for GCP infrastructure."""

import json
import sys

import pulumi
from pulumi import automation as auto

from config import (
    BACKEND_URL,
    PROJECT_NAME,
    STACK_NAME,
    configure_stack,
)

# Import module functions (each creates a group of resources)
from apis import enable_apis
from cloud_sql import create_cloud_sql
from iam import create_service_accounts
from secret_manager import create_secrets

from cloud_run import create_cloud_run_resources


def pulumi_program():
    """Inline Pulumi program defining all GCP infrastructure."""
    # 1. Enable required GCP APIs
    api_services = enable_apis()

    # 2. Cloud SQL: instance, databases, users
    sql = create_cloud_sql()

    # 3. Secrets: DB password, GSheets credentials, read-only user passwords
    secret_resources = create_secrets(sql)

    # 4. IAM: service accounts and role bindings
    iam = create_service_accounts()

    # 5. Cloud Run: Services and Jobs (images built separately via cloud-build-images)
    cr = create_cloud_run_resources(sql, secret_resources, iam)

    # Cloud Run exports
    pulumi.export("webservice_url", cr.webservice.uri)
    pulumi.export("prefect_server_url", cr.prefect_server.uri)
    pulumi.export("migration_job_name", cr.migration_job.name)

    # Exports
    pulumi.export("db_instance_name", sql.instance.name)
    pulumi.export("db_instance_connection_name", sql.instance.connection_name)
    pulumi.export("database_name", sql.database.name)
    pulumi.export("prefect_database_name", sql.prefect_database.name)
    for sa_name, sa in iam.service_accounts.items():
        pulumi.export(f"sa_{sa_name}_email", sa.email)


def get_stack() -> auto.Stack:
    """Create or select the Pulumi stack with programmatic config."""
    stack = auto.create_or_select_stack(
        stack_name=STACK_NAME,
        project_name=PROJECT_NAME,
        program=pulumi_program,
        opts=auto.LocalWorkspaceOptions(
            project_settings=auto.ProjectSettings(
                name=PROJECT_NAME,
                runtime="python",
                backend=auto.ProjectBackend(url=BACKEND_URL),
            ),
        ),
    )
    configure_stack(stack)
    return stack


def main():
    args = sys.argv[1:]
    command = args[0] if args else "preview"

    stack = get_stack()

    if command == "preview":
        result = stack.preview(on_output=print)
        print(f"\nPreview summary: {json.dumps(result.change_summary, indent=2)}")

    elif command == "up":
        result = stack.up(on_output=print)
        print(
            f"\nUpdate summary: {json.dumps(result.summary.resource_changes, indent=2)}"
        )

    elif command == "destroy":
        stack.destroy(on_output=print)
        print("Destroy complete.")

    elif command == "refresh":
        stack.refresh(on_output=print)
        print("Refresh complete.")

    elif command == "outputs":
        outputs = stack.outputs()
        for key, val in outputs.items():
            print(f"{key}: {val.value}")

    else:
        print(f"Unknown command: {command}")
        print("Usage: python deploy.py [preview|up|destroy|refresh|outputs]")
        sys.exit(1)


if __name__ == "__main__":
    main()
