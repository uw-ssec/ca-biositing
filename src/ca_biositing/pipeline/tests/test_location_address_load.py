import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch
from ca_biositing.pipeline.etl.load.location_address import load_location_address
from ca_biositing.datamodels.models import LocationAddress, Place

@patch("ca_biositing.pipeline.etl.load.location_address.get_engine")
def test_load_location_address_insert(mock_get_engine, session, engine):
    mock_get_engine.return_value = engine

    # 1. Setup Place data
    place1 = Place(geoid="06077", county_name="San Joaquin")
    place2 = Place(geoid="06019", county_name="Fresno")
    session.add_all([place1, place2])
    session.commit()

    # 2. Mock input DataFrame
    df = pd.DataFrame({
        'sampling_location': ['San Joaquin', 'Fresno'],
        'address_line1': ['123 Main St', None],
        'city': ['Stockton', 'Fresno'],
        'zip': ['95202', '93701'],
        'is_anonymous': [False, True]
    })

    # 3. Call Load
    load_location_address.fn(df)

    # 4. Verify results
    from sqlmodel import select
    results = session.exec(select(LocationAddress)).all()
    assert len(results) == 2

    # Stockton record
    stockton = session.exec(select(LocationAddress).where(LocationAddress.city == 'Stockton')).one()
    assert stockton.geography_id == "06077"
    assert stockton.address_line1 == "123 Main St"
    assert stockton.is_anonymous == False

    # Fresno record
    fresno = session.exec(select(LocationAddress).where(LocationAddress.city == 'Fresno')).one()
    assert fresno.geography_id == "06019"
    assert fresno.is_anonymous == True

@patch("ca_biositing.pipeline.etl.load.location_address.get_engine")
def test_load_location_address_update(mock_get_engine, session, engine):
    mock_get_engine.return_value = engine

    # 1. Setup existing data
    place1 = Place(geoid="06077", county_name="San Joaquin")
    session.add(place1)
    session.commit()

    existing_addr = LocationAddress(
        geography_id="06077",
        address_line1="123 Old St",
        city="Stockton",
        zip="95202",
        is_anonymous=False
    )
    session.add(existing_addr)
    session.commit()

    # 2. Mock input DataFrame with updated address but same lookup key (geography_id, address_line1, city, zip)
    # Wait, the lookup key in code is (geography_id, address_line1, city, zip)
    # So if we want to test UPDATE, we need to make sure the key MATCHES.
    df = pd.DataFrame({
        'sampling_location': ['San Joaquin'],
        'address_line1': ['123 Old St'], # Key matches
        'city': ['Stockton'],           # Key matches
        'zip': ['95202'],              # Key matches
        'is_anonymous': [True]         # Change this property
    })

    # 3. Call Load
    load_location_address.fn(df)

    # 4. Verify results
    from sqlmodel import select
    updated = session.exec(select(LocationAddress).where(
        LocationAddress.geography_id == "06077",
        LocationAddress.address_line1 == "123 Old St"
    )).one()
    assert updated.is_anonymous == True
    from sqlalchemy import func
    assert session.exec(select(func.count(LocationAddress.id))).one() == 1
