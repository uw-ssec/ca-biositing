#!/usr/bin/env python
"""CLI script to bootstrap the first admin user for JWT authentication.

Usage:
    python scripts/create_admin.py --username admin
    python scripts/create_admin.py --username admin --email admin@example.com

Password is read from the ADMIN_PASSWORD environment variable (for automation)
or prompted interactively via getpass when that variable is not set.

Requires DATABASE_URL environment variable (set by the pixi create-admin task).
"""

from __future__ import annotations

import argparse
import getpass
import os
import sys

from sqlmodel import Session, select

from ca_biositing.datamodels.database import get_engine
from ca_biositing.datamodels.models import ApiUser
from ca_biositing.webservice.services.auth_service import get_password_hash


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an admin user for the CA Biositing API.")
    parser.add_argument("--username", required=True, help="Admin username")
    parser.add_argument("--email", default=None, help="Admin email address (optional)")
    parser.add_argument("--full-name", default=None, dest="full_name", help="Admin full name (optional)")
    args = parser.parse_args()

    password = os.environ.get("ADMIN_PASSWORD") or getpass.getpass(
        f"Password for '{args.username}': "
    )

    engine = get_engine()
    with Session(engine) as session:
        existing = session.exec(select(ApiUser).where(ApiUser.username == args.username)).first()
        if existing:
            print(f"User '{args.username}' already exists — skipping creation.")
            sys.exit(0)

        user = ApiUser(
            username=args.username,
            hashed_password=get_password_hash(password),
            email=args.email,
            full_name=args.full_name,
            is_admin=True,
            disabled=False,
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    print(f"Admin user '{args.username}' created successfully (id={user.id}).")


if __name__ == "__main__":
    main()
