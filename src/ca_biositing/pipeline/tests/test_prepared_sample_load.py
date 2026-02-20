import pytest
import pandas as pd
from unittest.mock import patch
from ca_biositing.pipeline.etl.load.prepared_sample import load_prepared_sample
from ca_biositing.datamodels.models import PreparedSample

@patch("ca_biositing.pipeline.etl.load.prepared_sample.get_engine")
def test_load_prepared_sample_insert(mock_get_engine, session, engine):
    mock_get_engine.return_value = engine

    df = pd.DataFrame({
        'name': ['Prep 1', 'Prep 2'],
        'note': ['Note 1', 'Note 2']
    })

    # Call the task function directly
    load_prepared_sample.fn(df)

    # Verify records were inserted
    results = session.query(PreparedSample).all()
    assert len(results) == 2
    assert results[0].name == 'Prep 1'
    assert results[1].name == 'Prep 2'

@patch("ca_biositing.pipeline.etl.load.prepared_sample.get_engine")
def test_load_prepared_sample_update(mock_get_engine, session, engine):
    mock_get_engine.return_value = engine

    # Pre-insert a record
    existing = PreparedSample(name='Prep 1', note='Old Note')
    session.add(existing)
    session.commit()

    df = pd.DataFrame({
        'name': ['Prep 1'],
        'note': ['New Note']
    })

    # Call the task function directly
    load_prepared_sample.fn(df)

    # Verify record was updated
    updated = session.query(PreparedSample).filter(PreparedSample.name == 'Prep 1').one()
    assert updated.note == 'New Note'

    # Ensure no duplicate was created
    assert session.query(PreparedSample).count() == 1
