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
    # 1. Enable required GCP APIs — downstream resources depend on these.
    api_services = enable_apis()

    # 2. Cloud SQL: instance, databases, users
    sql = create_cloud_sql(depends_on=[api_services["sqladmin"]])

    # 3. Secrets: DB password, GSheets credentials, read-only user passwords
    secret_resources = create_secrets(
        sql, depends_on=[api_services["secretmanager"]]
    )

    # 4. IAM: service accounts and role bindings
    iam = create_service_accounts(
        depends_on=[api_services["iam"], api_services["cloudresourcemanager"]]
    )

    # 5. Cloud Run: Services and Jobs (images built separately via cloud-build-images)
    cr = create_cloud_run_resources(
        sql, secret_resources, iam, depends_on=[api_services["run"]]
    )

    # --- All exports centralized here ---
    # Cloud SQL
    pulumi.export("db_instance_name", sql.instance.name)
    pulumi.export("db_instance_connection_name", sql.instance.connection_name)
    pulumi.export("database_name", sql.database.name)
    pulumi.export("prefect_database_name", sql.prefect_database.name)

    # Secrets
    pulumi.export("db_password_secret_name", secret_resources.db_password_secret.name)
    pulumi.export("gsheets_secret_name", secret_resources.gsheets_secret.name)
    pulumi.export(
        "prefect_auth_secret_name", secret_resources.prefect_auth_secret.name
    )
    for username, secret in secret_resources.readonly_secrets.items():
        pulumi.export(f"ro_{username}_password_secret", secret.name)
    pulumi.export(
        "postgres_password_secret_name",
        secret_resources.postgres_password_secret.name,
    )

    # IAM
    for sa_name, sa in iam.service_accounts.items():
        pulumi.export(f"sa_{sa_name}_email", sa.email)

    # Cloud Run
    pulumi.export("webservice_url", cr.webservice.uri)
    pulumi.export("prefect_server_url", cr.prefect_server.uri)
    pulumi.export("migration_job_name", cr.migration_job.name)


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
        if result.summary:
            print(
                f"\nUpdate summary: {json.dumps(result.summary.resource_changes, indent=2)}"
            )
        else:
            print("\nUpdate completed (no summary available).")

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
