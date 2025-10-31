#!/bin/bash
# This script resets the Docker-based development environment.

# Exit immediately if a command exits with a non-zero status.
set -e

# Announce the action
echo "--- Stopping and removing all containers and volumes... ---"
docker-compose down -v

# Announce the next action
echo "--- Restarting all services... ---"
docker-compose up -d

# Announce the waiting period
echo "--- Waiting for the database to initialize... ---"
sleep 10 # Give the database container a moment to start up

# Announce the final action
echo "--- Applying all database migrations... ---"
docker-compose exec -T app pixi run alembic upgrade head

echo "--- Database reset complete. Your environment is ready. ---"
