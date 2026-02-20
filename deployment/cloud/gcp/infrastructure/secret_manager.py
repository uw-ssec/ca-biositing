"""Secret Manager resources, database users, and password management."""

from dataclasses import dataclass, field
from typing import Sequence

import pulumi
import pulumi_gcp as gcp
import pulumi_random as random

from cloud_sql import CloudSQLResources
from config import DB_USER, READONLY_USERS


@dataclass
class SecretResources:
    db_password: random.RandomPassword
    db_user: gcp.sql.User
    db_password_secret: gcp.secretmanager.Secret
    gsheets_secret: gcp.secretmanager.Secret
    prefect_auth_password: random.RandomPassword = None
    prefect_auth_secret: gcp.secretmanager.Secret = None
    readonly_users: dict = field(default_factory=dict)
    readonly_passwords: dict = field(default_factory=dict)
    readonly_secrets: dict = field(default_factory=dict)
    postgres_password: random.RandomPassword = None
    postgres_user: gcp.sql.User = None
    postgres_password_secret: gcp.secretmanager.Secret = None


def create_secrets(
    sql: CloudSQLResources,
    depends_on: Sequence[pulumi.Resource] | None = None,
) -> SecretResources:
    """Create Secret Manager secrets, database users, and passwords."""
    secret_opts = pulumi.ResourceOptions(depends_on=depends_on or [])

    # Primary database user password
    db_password = random.RandomPassword(
        "db-password",
        length=32,
        special=False,
    )

    # Create the primary database user
    db_user = gcp.sql.User(
        "db-user",
        name=DB_USER,
        instance=sql.instance.name,
        password=db_password.result,
    )

    # Store the DB password in Secret Manager
    db_password_secret = gcp.secretmanager.Secret(
        "db-password-secret",
        secret_id="biocirv-staging-db-password",
        replication=gcp.secretmanager.SecretReplicationArgs(
            auto=gcp.secretmanager.SecretReplicationAutoArgs(),
        ),
        opts=secret_opts,
    )

    gcp.secretmanager.SecretVersion(
        "db-password-version",
        secret=db_password_secret.id,
        secret_data=db_password.result,
    )

    # Google Sheets credentials secret (version added manually post-deploy)
    gsheets_secret = gcp.secretmanager.Secret(
        "gsheets-credentials-secret",
        secret_id="biocirv-staging-gsheets-credentials",
        replication=gcp.secretmanager.SecretReplicationArgs(
            auto=gcp.secretmanager.SecretReplicationAutoArgs(),
        ),
        opts=secret_opts,
    )

    # Prefect server auth credential (HTTP Basic Auth)
    prefect_auth_password = random.RandomPassword(
        "prefect-auth-password",
        length=32,
        special=False,
    )

    prefect_auth_secret = gcp.secretmanager.Secret(
        "prefect-auth-secret",
        secret_id="biocirv-staging-prefect-auth",
        replication=gcp.secretmanager.SecretReplicationArgs(
            auto=gcp.secretmanager.SecretReplicationAutoArgs(),
        ),
        opts=secret_opts,
    )

    gcp.secretmanager.SecretVersion(
        "prefect-auth-version",
        secret=prefect_auth_secret.id,
        secret_data=pulumi.Output.concat("admin:", prefect_auth_password.result),
    )

    # Read-only users
    readonly_users = {}
    readonly_passwords = {}
    readonly_secrets = {}

    for username in READONLY_USERS:
        # Generate password for read-only user
        ro_password = random.RandomPassword(
            f"ro-password-{username}",
            length=32,
            special=False,
        )
        readonly_passwords[username] = ro_password

        # Create the Cloud SQL user
        ro_user = gcp.sql.User(
            f"ro-user-{username}",
            name=username,
            instance=sql.instance.name,
            password=ro_password.result,
            deletion_policy="ABANDON",
        )
        readonly_users[username] = ro_user

        # Store password in Secret Manager
        ro_secret = gcp.secretmanager.Secret(
            f"ro-password-secret-{username}",
            secret_id=f"biocirv-staging-ro-{username}",
            replication=gcp.secretmanager.SecretReplicationArgs(
                auto=gcp.secretmanager.SecretReplicationAutoArgs(),
            ),
            opts=secret_opts,
        )
        readonly_secrets[username] = ro_secret

        gcp.secretmanager.SecretVersion(
            f"ro-password-version-{username}",
            secret=ro_secret.id,
            secret_data=ro_password.result,
        )

    # Postgres superuser password
    postgres_password = random.RandomPassword(
        "postgres-password",
        length=32,
        special=False,
    )

    # Manage the built-in postgres user (Pulumi will adopt the existing user)
    postgres_user = gcp.sql.User(
        "postgres-user",
        name="postgres",
        instance=sql.instance.name,
        password=postgres_password.result,
        deletion_policy="ABANDON",
    )

    # Store the postgres password in Secret Manager
    postgres_password_secret = gcp.secretmanager.Secret(
        "postgres-password-secret",
        secret_id="biocirv-staging-postgres-password",
        replication=gcp.secretmanager.SecretReplicationArgs(
            auto=gcp.secretmanager.SecretReplicationAutoArgs(),
        ),
        opts=secret_opts,
    )

    gcp.secretmanager.SecretVersion(
        "postgres-password-version",
        secret=postgres_password_secret.id,
        secret_data=postgres_password.result,
    )

    return SecretResources(
        db_password=db_password,
        db_user=db_user,
        db_password_secret=db_password_secret,
        gsheets_secret=gsheets_secret,
        prefect_auth_password=prefect_auth_password,
        prefect_auth_secret=prefect_auth_secret,
        readonly_users=readonly_users,
        readonly_passwords=readonly_passwords,
        readonly_secrets=readonly_secrets,
        postgres_password=postgres_password,
        postgres_user=postgres_user,
        postgres_password_secret=postgres_password_secret,
    )
