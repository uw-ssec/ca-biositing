-- Create Prefect database for workflow orchestration
-- This database is used by Prefect server to store workflow metadata,
-- run history, and task state information.
--
-- Usage:
--   psql -U $POSTGRES_USER -f create_prefect_db.sql
--
-- Note: This script is idempotent and can be run multiple times safely.

-- Create the prefect_db database if it doesn't exist
SELECT 'CREATE DATABASE prefect_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'prefect_db')\gexec

-- Grant all privileges on prefect_db to the POSTGRES_USER
-- Note: Replace ${POSTGRES_USER} with the actual username when running manually,
-- or use the environment variable if running through docker-compose
\c prefect_db

-- Grant privileges to the database owner
GRANT ALL PRIVILEGES ON DATABASE prefect_db TO CURRENT_USER;

-- Grant default privileges for future tables and sequences
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO CURRENT_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO CURRENT_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO CURRENT_USER;

-- Display confirmation
\echo 'Successfully created prefect_db and granted privileges'
\echo 'Database: prefect_db'
\echo 'Owner: ' :USER
