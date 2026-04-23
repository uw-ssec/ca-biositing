"""Apply local materialized view updates without Alembic migrations.

This script is intended for rapid local validation while migration plans are still
being staged. It recompiles SQL from current SQLAlchemy view definitions and
recreates the selected materialized views in the local Docker DB.
"""

from sqlalchemy import text
from sqlalchemy.dialects import postgresql

from ca_biositing.datamodels.database import get_engine
from ca_biositing.datamodels.data_portal_views import mv_biomass_end_uses, mv_biomass_search


def _compiled_sql(select_stmt) -> str:
    return str(
        select_stmt.compile(
            dialect=postgresql.dialect(),
            compile_kwargs={"literal_binds": True},
        )
    )


def main() -> None:
    end_uses_sql = _compiled_sql(mv_biomass_end_uses)
    search_sql = _compiled_sql(mv_biomass_search)

    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_end_uses CASCADE"))
        conn.execute(text("DROP MATERIALIZED VIEW IF EXISTS data_portal.mv_biomass_search CASCADE"))

        conn.execute(text(f"CREATE MATERIALIZED VIEW data_portal.mv_biomass_search AS {search_sql}"))
        conn.execute(
            text(
                "CREATE UNIQUE INDEX idx_mv_biomass_search_id ON data_portal.mv_biomass_search (id)"
            )
        )
        conn.execute(
            text(
                "CREATE INDEX idx_mv_biomass_search_search_vector ON data_portal.mv_biomass_search USING GIN (search_vector)"
            )
        )
        conn.execute(
            text(
                "CREATE INDEX idx_mv_biomass_search_name_trgm ON data_portal.mv_biomass_search USING GIN (name gin_trgm_ops)"
            )
        )
        conn.execute(
            text(
                "CREATE INDEX idx_mv_biomass_search_resource_class ON data_portal.mv_biomass_search (resource_class)"
            )
        )
        conn.execute(
            text(
                "CREATE INDEX idx_mv_biomass_search_resource_subclass ON data_portal.mv_biomass_search (resource_subclass)"
            )
        )
        conn.execute(
            text(
                "CREATE INDEX idx_mv_biomass_search_primary_product ON data_portal.mv_biomass_search (primary_product)"
            )
        )

        conn.execute(text(f"CREATE MATERIALIZED VIEW data_portal.mv_biomass_end_uses AS {end_uses_sql}"))
        conn.execute(
            text(
                "CREATE UNIQUE INDEX idx_mv_biomass_end_uses_resource_use_case ON data_portal.mv_biomass_end_uses (resource_id, use_case)"
            )
        )
        conn.execute(
            text(
                "CREATE INDEX idx_mv_biomass_end_uses_resource_id ON data_portal.mv_biomass_end_uses (resource_id)"
            )
        )

        conn.execute(text("GRANT USAGE ON SCHEMA data_portal TO biocirv_readonly"))
        conn.execute(text("GRANT SELECT ON data_portal.mv_biomass_search TO biocirv_readonly"))
        conn.execute(text("GRANT SELECT ON data_portal.mv_biomass_end_uses TO biocirv_readonly"))

    print("Applied local updates for mv_biomass_search and mv_biomass_end_uses")


if __name__ == "__main__":
    main()
