import pytest
import pandas as pd
from unittest.mock import patch
from ca_biositing.pipeline.etl.load.field_sample import load_field_sample
from ca_biositing.datamodels.schemas.generated.ca_biositing import FieldSample

@patch("ca_biositing.pipeline.etl.load.field_sample.get_local_engine")
def test_load_field_sample_insert(mock_get_engine, session, engine):
    mock_get_engine.return_value = engine

    df = pd.DataFrame({
        'name': ['Sample 1', 'Sample 2'],
        'note': ['Note 1', 'Note 2']
    })

    # Call the task function directly
    load_field_sample.fn(df)

    # Verify records were inserted
    results = session.query(FieldSample).all()
    assert len(results) == 2
    assert results[0].name == 'Sample 1'
    assert results[1].name == 'Sample 2'

@patch("ca_biositing.pipeline.etl.load.field_sample.get_local_engine")
def test_load_field_sample_update(mock_get_engine, session, engine):
    mock_get_engine.return_value = engine

    # Pre-insert a record
    existing = FieldSample(name='Sample 1', note='Old Note')
    session.add(existing)
    session.commit()

    df = pd.DataFrame({
        'name': ['Sample 1'],
        'note': ['New Note']
    })

    # Call the task function directly
    load_field_sample.fn(df)

    # Verify record was updated
    updated = session.query(FieldSample).filter(FieldSample.name == 'Sample 1').one()
    assert updated.note == 'New Note'

    # Ensure no duplicate was created
    assert session.query(FieldSample).count() == 1
