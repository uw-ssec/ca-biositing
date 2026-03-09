"""
Tests for seed_commodity_mappings.py — specifically the dual resource/primary_ag_product
lookup introduced in TODO 6.

These tests use mocks to avoid any database dependency, following the same pattern
as tests/USDA/test_api_names.py.

Run with:
    pixi run test -- src/ca_biositing/pipeline/tests/test_seeding.py
"""

import os
from unittest.mock import MagicMock

# ── CSV helper ────────────────────────────────────────────────────────────────

_CSV_HEADER = "resource_name,commodity_name,api_name,usda_code,match_tier,note\n"


def _write_csv(directory: str, rows: list[tuple]) -> str:
    """Write test CSV rows to a file and return its path."""
    path = os.path.join(directory, "test_mappings.csv")
    with open(path, "w") as f:
        f.write(_CSV_HEADER)
        for row in rows:
            f.write(",".join(str(v) for v in row) + "\n")
    return path


# ── Mock DB helpers ───────────────────────────────────────────────────────────

def _make_mock_conn(
    resource_ids: dict[str, int],
    pap_ids: dict[str, int],
    commodity_ids: dict[str, int],
) -> tuple[MagicMock, list[dict]]:
    """
    Build a mock SQLAlchemy connection with scripted query results.

    Args:
        resource_ids:   {lowercase_name: id} rows present in the resource table
        pap_ids:        {lowercase_name: id} rows present in the primary_ag_product table
        commodity_ids:  {lowercase_name: id} rows present in the usda_commodity table

    Returns:
        (mock_conn, inserted_maps) where inserted_maps is a list of param dicts
        captured from INSERT INTO resource_usda_commodity_map calls.
    """
    mock_conn = MagicMock()
    inserted_maps: list[dict] = []

    def _execute(query, params=None):
        result = MagicMock()
        qs = str(query)
        p = params or {}

        if "FROM resource WHERE" in qs:
            row_id = resource_ids.get(p.get("name"))
            result.fetchone.return_value = (row_id,) if row_id is not None else None

        elif "FROM primary_ag_product WHERE" in qs:
            row_id = pap_ids.get(p.get("name"))
            result.fetchone.return_value = (row_id,) if row_id is not None else None

        elif "FROM usda_commodity WHERE" in qs:
            # The seeder uses :name on the first check, :commodity_name on the second
            name = p.get("name") or p.get("commodity_name")
            row_id = commodity_ids.get(name)
            result.fetchone.return_value = (row_id,) if row_id is not None else None

        elif "INSERT INTO resource_usda_commodity_map" in qs:
            inserted_maps.append(dict(p))
            result.fetchone.return_value = None

        else:
            # UPDATE usda_commodity, INSERT usda_commodity, DELETE …
            result.fetchone.return_value = None
            result.fetchall.return_value = []
            result.scalar.return_value = 0

        return result

    mock_conn.execute.side_effect = _execute
    mock_conn.begin.return_value = MagicMock()   # transaction mock — commit/rollback are no-ops
    return mock_conn, inserted_maps


def _make_mock_engine(mock_conn: MagicMock) -> MagicMock:
    """Wrap a mock connection in a mock engine that supports `with engine.connect() as conn:`."""
    engine = MagicMock()
    engine.connect.return_value.__enter__.return_value = mock_conn
    engine.connect.return_value.__exit__.return_value = False
    return engine


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestSeederDualLookup:
    """
    Verify the resource / primary_ag_product dual-lookup added in TODO 6.

    Each test writes a minimal CSV, passes a scripted engine mock, then checks
    the params that were passed to the INSERT INTO resource_usda_commodity_map
    statement.
    """

    def test_resource_row_sets_resource_id(self, tmp_path):
        """When resource_name exists in the resource table, resource_id is populated and pap_id is None."""
        from ca_biositing.pipeline.utils.seed_commodity_mappings import seed_commodity_mappings_from_csv

        csv_path = _write_csv(str(tmp_path), [
            ("alfalfa hay", "alfalfa", "ALFALFA", 12345, "EXACT", "test note"),
        ])

        mock_conn, inserted_maps = _make_mock_conn(
            resource_ids={"alfalfa hay": 42},
            pap_ids={},
            commodity_ids={"alfalfa": 99},
        )
        engine = _make_mock_engine(mock_conn)

        result = seed_commodity_mappings_from_csv(csv_path=csv_path, engine=engine)

        assert result is True
        assert len(inserted_maps) == 1
        assert inserted_maps[0]["resource_id"] == 42
        assert inserted_maps[0]["pap_id"] is None

    def test_pap_row_sets_pap_id_when_resource_missing(self, tmp_path):
        """
        When resource_name is NOT in resource but IS in primary_ag_product,
        primary_ag_product_id (pap_id) is populated and resource_id is None.
        """
        from ca_biositing.pipeline.utils.seed_commodity_mappings import seed_commodity_mappings_from_csv

        csv_path = _write_csv(str(tmp_path), [
            ("corn stover", "corn", "CORN", 11111, "EXACT", ""),
        ])

        mock_conn, inserted_maps = _make_mock_conn(
            resource_ids={},                    # name NOT in resource
            pap_ids={"corn stover": 77},        # but IS in primary_ag_product
            commodity_ids={"corn": 55},
        )
        engine = _make_mock_engine(mock_conn)

        result = seed_commodity_mappings_from_csv(csv_path=csv_path, engine=engine)

        assert result is True
        assert len(inserted_maps) == 1
        assert inserted_maps[0]["pap_id"] == 77
        assert inserted_maps[0]["resource_id"] is None

    def test_resource_lookup_takes_priority_over_pap(self, tmp_path):
        """
        When resource_name exists in BOTH tables, the resource table wins
        (resource_id is set, pap_id remains None).
        """
        from ca_biositing.pipeline.utils.seed_commodity_mappings import seed_commodity_mappings_from_csv

        csv_path = _write_csv(str(tmp_path), [
            ("wheat straw", "wheat", "WHEAT", 22222, "EXACT", ""),
        ])

        mock_conn, inserted_maps = _make_mock_conn(
            resource_ids={"wheat straw": 10},   # found here first
            pap_ids={"wheat straw": 20},        # would also match here
            commodity_ids={"wheat": 5},
        )
        engine = _make_mock_engine(mock_conn)

        result = seed_commodity_mappings_from_csv(csv_path=csv_path, engine=engine)

        assert result is True
        assert len(inserted_maps) == 1
        assert inserted_maps[0]["resource_id"] == 10
        assert inserted_maps[0]["pap_id"] is None

    def test_missing_row_is_skipped(self, tmp_path):
        """When resource_name is in neither table, the row is skipped and no INSERT is emitted."""
        from ca_biositing.pipeline.utils.seed_commodity_mappings import seed_commodity_mappings_from_csv

        csv_path = _write_csv(str(tmp_path), [
            ("ghost crop", "wheat", "WHEAT", 22222, "MANUAL", ""),
        ])

        mock_conn, inserted_maps = _make_mock_conn(
            resource_ids={},
            pap_ids={},
            commodity_ids={"wheat": 11},
        )
        engine = _make_mock_engine(mock_conn)

        result = seed_commodity_mappings_from_csv(csv_path=csv_path, engine=engine)

        assert result is True
        assert len(inserted_maps) == 0

    def test_unmapped_rows_excluded_before_db_lookups(self, tmp_path):
        """Rows with match_tier == UNMAPPED must be filtered out before any DB queries are issued."""
        from ca_biositing.pipeline.utils.seed_commodity_mappings import seed_commodity_mappings_from_csv

        csv_path = _write_csv(str(tmp_path), [
            ("some resource", "some commodity", "NONE", 0, "UNMAPPED", ""),
        ])

        mock_conn, inserted_maps = _make_mock_conn(
            resource_ids={"some resource": 1},
            pap_ids={},
            commodity_ids={},
        )
        engine = _make_mock_engine(mock_conn)

        result = seed_commodity_mappings_from_csv(csv_path=csv_path, engine=engine)

        assert result is True
        assert len(inserted_maps) == 0

    def test_mixed_csv_handles_both_types_correctly(self, tmp_path):
        """
        A CSV containing both a resource row and a primary_ag_product row produces
        two correctly typed INSERTs.
        """
        from ca_biositing.pipeline.utils.seed_commodity_mappings import seed_commodity_mappings_from_csv

        csv_path = _write_csv(str(tmp_path), [
            ("alfalfa hay", "alfalfa", "ALFALFA", 12345, "EXACT", "resource type"),
            ("corn stover", "corn",    "CORN",    11111, "EXACT", "pap type"),
        ])

        mock_conn, inserted_maps = _make_mock_conn(
            resource_ids={"alfalfa hay": 10},
            pap_ids={"corn stover": 20},
            commodity_ids={"alfalfa": 1, "corn": 2},
        )
        engine = _make_mock_engine(mock_conn)

        result = seed_commodity_mappings_from_csv(csv_path=csv_path, engine=engine)

        assert result is True
        assert len(inserted_maps) == 2

        resource_row = next(m for m in inserted_maps if m.get("resource_id") == 10)
        pap_row      = next(m for m in inserted_maps if m.get("pap_id") == 20)

        assert resource_row["pap_id"] is None
        assert pap_row["resource_id"] is None
