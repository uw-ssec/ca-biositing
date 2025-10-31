"""Tests for geographic location data models."""

from decimal import Decimal

from ca_biositing.datamodels.geographic_locations import (
    GeographicLocation,
    StreetAddress,
    City,
    Zip,
    County,
    FIPS,
    State,
    Region,
    LocationResolution,
)


def test_geographic_location_creation():
    """Test creating a GeographicLocation instance."""
    location = GeographicLocation(
        latitude=Decimal("37.7749"),
        longitude=Decimal("-122.4194"),
        is_anonymous=False
    )
    assert location.latitude == Decimal("37.7749")
    assert location.longitude == Decimal("-122.4194")
    assert location.is_anonymous is False


def test_street_address_creation():
    """Test creating a StreetAddress instance."""
    address = StreetAddress(street_address="123 Main St")
    assert address.street_address == "123 Main St"


def test_city_creation():
    """Test creating a City instance."""
    city = City(city_name="San Francisco")
    assert city.city_name == "San Francisco"


def test_zip_creation():
    """Test creating a Zip instance."""
    zip_code = Zip(zip_code="94102")
    assert zip_code.zip_code == "94102"


def test_county_creation():
    """Test creating a County instance."""
    county = County(county_name="San Francisco County")
    assert county.county_name == "San Francisco County"


def test_fips_creation():
    """Test creating a FIPS instance."""
    fips = FIPS(fips_description="06075")
    assert fips.fips_description == "06075"


def test_state_creation():
    """Test creating a State instance."""
    state = State(state_name="California")
    assert state.state_name == "California"


def test_region_creation():
    """Test creating a Region instance."""
    region = Region(region_name="West Coast")
    assert region.region_name == "West Coast"


def test_location_resolution_creation():
    """Test creating a LocationResolution instance."""
    resolution = LocationResolution(resolution_type="GPS")
    assert resolution.resolution_type == "GPS"


def test_city_persistence(session):
    """Test saving and retrieving a City instance from database."""
    city = City(city_name="Sacramento")
    session.add(city)
    session.commit()
    session.refresh(city)

    assert city.city_id is not None

    retrieved = session.get(City, city.city_id)
    assert retrieved is not None
    assert retrieved.city_name == "Sacramento"


def test_state_persistence(session):
    """Test saving and retrieving a State instance from database."""
    state = State(state_name="California")
    session.add(state)
    session.commit()
    session.refresh(state)

    assert state.state_id is not None

    retrieved = session.get(State, state.state_id)
    assert retrieved is not None
    assert retrieved.state_name == "California"
