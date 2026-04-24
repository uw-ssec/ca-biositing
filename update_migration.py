#!/usr/bin/env python3
"""Script to update the migration file with corrected SQL."""

import sys
from pathlib import Path

# Read the corrected SQL from the temp file
sql_file = Path("/tmp/mv_biomass_search_sql.txt")
if not sql_file.exists():
    print("ERROR: SQL file not found at /tmp/mv_biomass_search_sql.txt")
    sys.exit(1)

corrected_sql = sql_file.read_text().strip()

# Create the migration file content
migration_content = '''"""Update biomass materialized views for qualitative end-use changes.

Revision ID: d2b6b2a7c9d1
Revises: 60b08397200f
Create Date: 2026-04-15 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d2b6b2a7c9d1"
down_revision: Union[str, Sequence[str], None] = "60b08397200f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


MV_BIOMASS_END_USES_SQL = """
SELECT resource_end_use_record.resource_id, resource.name AS resource_name, coalesce(use_case.name, 'unknown') AS use_case, CAST(avg(anon_1.percentage_low) AS FLOAT) AS percentage_low, CAST(avg(anon_1.percentage_high) AS FLOAT) AS percentage_high, CAST(max(anon_1.trend) AS TEXT) AS trend, CAST(avg(anon_1.value_low_usd) AS FLOAT) AS value_low_usd, CAST(avg(anon_1.value_high_usd) AS FLOAT) AS value_high_usd, CAST(max(anon_1.value_unit) AS TEXT) AS value_notes
FROM resource_end_use_record JOIN resource ON resource_end_use_record.resource_id = resource.id LEFT OUTER JOIN use_case ON resource_end_use_record.use_case_id = use_case.id LEFT OUTER JOIN (SELECT observation.record_id AS record_id, avg(CASE WHEN (lower(parameter.name) = 'resource_use_perc_low') THEN observation.value END) AS percentage_low, avg(CASE WHEN (lower(parameter.name) = 'resource_use_perc_high') THEN observation.value END) AS percentage_high, avg(CASE WHEN (lower(parameter.name) = 'resource_value_low') THEN observation.value END) AS value_low_usd, avg(CASE WHEN (lower(parameter.name) = 'resource_value_high') THEN observation.value END) AS value_high_usd, max(CASE WHEN (lower(parameter.name) = 'resource_use_perc_low') THEN unit.name END) AS unit, max(CASE WHEN (lower(parameter.name) = 'resource_use_trend') THEN CAST(observation.note AS VARCHAR) END) AS trend, max(CASE WHEN (lower(parameter.name) IN ('resource_value_low', 'resource_value_high')) THEN unit.name END) AS value_unit
FROM observation JOIN parameter ON observation.parameter_id = parameter.id LEFT OUTER JOIN unit ON observation.unit_id = unit.id
WHERE lower(observation.record_type) = 'resource_end_use_record' GROUP BY observation.record_id) AS anon_1 ON CAST(resource_end_use_record.id AS VARCHAR) = anon_1.record_id
WHERE resource_end_use_record.resource_id IS NOT NULL GROUP BY resource_end_use_record.resource_id, resource.name, coalesce(use_case.name, 'unknown')
"""


MV_BIOMASS_SEARCH_SQL = """
''' + corrected_sql + '''
"""


def upgrade() -> None:
    """Recreate biomass materialized views from frozen SQL snapshots."""
    op.execute("DROP INDEX IF EXISTS data_portal.idx_mv_biomass_search_primary_product CASCADE")
    op.execute("DROP INDEX IF EXISTS data_portal.idx_mv_biomass_search_resource_subclass CASCADE")
    op.execute("DROP INDEX IF EXISTS data_portal.idx_mv_biomass_search_resource_class CASCADE")
    op.execute("DROP INDEX IF EXISTS data_portal.idx_mv_biomass_search_name_trgm CASCADE")
    op.execute("DROP INDEX IF EXISTS data_portal.idx_mv_biomass_search_search_vector CASCADE")
    op.execute("DROP INDEX IF EXISTS data_portal.idx_mv_biomass_search_id CASCADE")
    op.execute("DROP INDEX IF EXISTS data_portal.idx_mv_biomass_end_uses_resource_id CASCADE")
    op.execute("DROP INDEX IF EXISTS data_portal.idx_mv_biomass_end_uses_resource_use_case CASCADE")

    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_end_uses CASCADE")

    op.execute(f"CREATE MATERIALIZED VIEW data_portal.mv_biomass_search AS {MV_BIOMASS_SEARCH_SQL}")
    op.execute("CREATE UNIQUE INDEX idx_mv_biomass_search_id ON data_portal.mv_biomass_search (id)")
    op.execute("CREATE INDEX idx_mv_biomass_search_search_vector ON data_portal.mv_biomass_search USING GIN (search_vector)")
    op.execute("CREATE INDEX idx_mv_biomass_search_name_trgm ON data_portal.mv_biomass_search USING GIN (name gin_trgm_ops)")
    op.execute("CREATE INDEX idx_mv_biomass_search_resource_class ON data_portal.mv_biomass_search (resource_class)")
    op.execute("CREATE INDEX idx_mv_biomass_search_resource_subclass ON data_portal.mv_biomass_search (resource_subclass)")
    op.execute("CREATE INDEX idx_mv_biomass_search_primary_product ON data_portal.mv_biomass_search (primary_product)")

    op.execute(f"CREATE MATERIALIZED VIEW data_portal.mv_biomass_end_uses AS {MV_BIOMASS_END_USES_SQL}")
    op.execute("CREATE UNIQUE INDEX idx_mv_biomass_end_uses_resource_use_case ON data_portal.mv_biomass_end_uses (resource_id, use_case)")
    op.execute("CREATE INDEX idx_mv_biomass_end_uses_resource_id ON data_portal.mv_biomass_end_uses (resource_id)")

    op.execute("GRANT USAGE ON SCHEMA data_portal TO biocirv_readonly")
    op.execute("GRANT SELECT ON data_portal.mv_biomass_search TO biocirv_readonly")
    op.execute("GRANT SELECT ON data_portal.mv_biomass_end_uses TO biocirv_readonly")


def downgrade() -> None:
    """Drop biomass materialized views created by this revision."""
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_end_uses CASCADE")
'''

# Write the migration file
migration_file = Path("alembic/versions/d2b6b2a7c9d1_update_biomass_materialized_views_for_qualitative.py")
migration_file.write_text(migration_content)
print(f"Updated migration file: {migration_file}")
