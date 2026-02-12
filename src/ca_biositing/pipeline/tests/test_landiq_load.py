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
from ca_biositing.pipeline.utils.lookup_utils import fetch_lookup_ids
from ca_biositing.datamodels.models import LandiqRecord, Polygon, DataSource, PrimaryAgProduct

def test_fetch_polygon_ids_by_geoms(session):
    # Setup: Add some polygons
    p1 = Polygon(geom="POINT(0 0)")
    p2 = Polygon(geom="POINT(1 1)")
    session.add_all([p1, p2])
    session.commit()

    geoms = ["POINT(0 0)", "POINT(1 1)", "POINT(2 2)"]
    poly_map = fetch_polygon_ids_by_geoms(session, geoms)

    assert len(poly_map) == 2
    # Keys may be WKBElement (from GeoAlchemy2) or strings; verify IDs are present
    returned_ids = set(poly_map.values())
    assert p1.id in returned_ids
    assert p2.id in returned_ids

@patch("ca_biositing.pipeline.etl.load.landiq.get_local_engine")
def test_load_landiq_record_optimized(mock_get_engine, session, engine):
    mock_get_engine.return_value = engine

    # Setup reference data
    from ca_biositing.datamodels.models import Dataset
    ds = Dataset(name="Test Dataset")
    crop = PrimaryAgProduct(name="Almonds")
    session.add_all([ds, crop])
    session.commit()
    session.refresh(ds)

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
        # Mock fetch_lookup_ids where it is imported in landiq.py
        # We use the full path to where it's used in the task
        with patch("ca_biositing.pipeline.utils.lookup_utils.fetch_lookup_ids", spec=fetch_lookup_ids) as mock_lookup:
            mock_lookup.side_effect = [
                {"Almonds": crop.id},  # First call for crops
                {"Test Dataset": ds.id}  # Second call for datasets
            ]

            # We need to mock the polygon fetching logic inside load_landiq_record
            # Since it doesn't call fetch_polygon_ids_by_geoms but has its own loop
            # We mock the session.execute().all() to return a polygon ID
            mock_result = MagicMock()
            mock_result.all.return_value = [MagicMock(id=1, geom='POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))')]

            # We need to mock the Session class that is used inside load_landiq_record
            with patch("ca_biositing.pipeline.etl.load.landiq.Session", create=True) as mock_session_cls:
                mock_session = mock_session_cls.return_value.__enter__.return_value
                mock_session.execute.return_value = mock_result

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
