import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from ca_biositing.pipeline.etl.load.landiq import (
    bulk_insert_polygons_ignore,
    fetch_polygon_ids_by_geoms,
    bulk_upsert_landiq_records,
    load_landiq_record
)
from ca_biositing.datamodels.schemas.generated.ca_biositing import LandiqRecord, Polygon, DataSource, PrimaryAgProduct

def test_fetch_polygon_ids_by_geoms(session):
    # Setup: Add some polygons
    p1 = Polygon(geom="POINT(0 0)")
    p2 = Polygon(geom="POINT(1 1)")
    session.add_all([p1, p2])
    session.commit()

    geoms = ["POINT(0 0)", "POINT(1 1)", "POINT(2 2)"]
    poly_map = fetch_polygon_ids_by_geoms(session, geoms)

    assert len(poly_map) == 2
    assert poly_map["POINT(0 0)"] == p1.id
    assert poly_map["POINT(1 1)"] == p2.id
    assert "POINT(2 2)" not in poly_map

@patch("ca_biositing.pipeline.etl.load.landiq.get_local_engine")
def test_load_landiq_record_optimized(mock_get_engine, session, engine):
    mock_get_engine.return_value = engine

    # Setup reference data
    ds = DataSource(name="Test Dataset")
    crop = PrimaryAgProduct(name="Almonds")
    session.add_all([ds, crop])
    session.commit()

    # Create test DataFrame
    df = pd.DataFrame({
        'record_id': ['REC1', 'REC2'],
        'dataset_id': ['Test Dataset', 'Test Dataset'],
        'geometry': ['POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))', 'POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'],
        'main_crop': ['Almonds', 'Almonds'],
        'acres': [10.5, 20.0],
        'etl_run_id': ['RUN1', 'RUN1']
    })

    # We need to mock the PostgreSQL-specific 'insert' because we are using SQLite for tests
    # SQLite doesn't support 'on_conflict_do_nothing' or 'on_conflict_do_update' in the same way
    # So we will mock the bulk functions to verify they are called correctly,
    # or just test the logic around them.

    with patch("ca_biositing.pipeline.etl.load.landiq.bulk_insert_polygons_ignore") as mock_poly_ins, \
         patch("ca_biositing.pipeline.etl.load.landiq.bulk_upsert_landiq_records") as mock_upsert:

        # Mock poly_map return
        with patch("ca_biositing.pipeline.etl.load.landiq.fetch_polygon_ids_by_geoms") as mock_fetch_poly:
            mock_fetch_poly.return_value = {'POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))': 1}

            load_landiq_record.fn(df)

            assert mock_poly_ins.called
            assert mock_upsert.called

            # Verify records passed to upsert
            args, _ = mock_upsert.call_args
            records = args[1]
            assert len(records) == 2
            assert records[0]['record_id'] == 'REC1'
            assert records[0]['polygon_id'] == 1
            assert records[0]['acres'] == 10.5
