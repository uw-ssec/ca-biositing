"""Tests for biomass-related data models."""

from decimal import Decimal
from datetime import datetime

from ca_biositing.datamodels.biomass import (
    Biomass,
    BiomassTest,
    BiomassType,
    PrimaryProduct,
    BiomassAvailability,
    BiomassQuality,
    BiomassPrice,
    FieldSample,
    HarvestMethod,
    CollectionMethod,
    FieldStorage,
)


def test_biomass_creation():
    """Test creating a Biomass instance."""
    biomass = Biomass(
        biomass_name="Test Biomass",
        biomass_notes="Test notes"
    )
    assert biomass.biomass_name == "Test Biomass"
    assert biomass.biomass_notes == "Test notes"
    assert biomass.biomass_id is None


def test_biomass_test_creation():
    """Test creating a BiomassTest instance."""
    biomass_test = BiomassTest(
        biomass_test_name="Test Name",
        biomass_test_notes="Test notes"
    )
    assert biomass_test.biomass_test_name == "Test Name"
    assert biomass_test.biomass_test_notes == "Test notes"


def test_biomass_type_creation():
    """Test creating a BiomassType instance."""
    biomass_type = BiomassType(biomass_type="Crop by-product")
    assert biomass_type.biomass_type == "Crop by-product"


def test_primary_product_creation():
    """Test creating a PrimaryProduct instance."""
    product = PrimaryProduct(primary_product_name="Ethanol")
    assert product.primary_product_name == "Ethanol"


def test_biomass_availability_creation():
    """Test creating a BiomassAvailability instance."""
    availability = BiomassAvailability(
        biomass_id=1,
        from_month=Decimal("1"),
        to_month=Decimal("12"),
        kg_avg=Decimal("1000.50"),
    )
    assert availability.biomass_id == 1
    assert availability.from_month == Decimal("1")
    assert availability.kg_avg == Decimal("1000.50")


def test_biomass_quality_creation():
    """Test creating a BiomassQuality instance."""
    quality = BiomassQuality(
        biomass_id=1,
        expected_quality="High",
        convertibility="Easy"
    )
    assert quality.biomass_id == 1
    assert quality.expected_quality == "High"


def test_biomass_price_creation():
    """Test creating a BiomassPrice instance."""
    price = BiomassPrice(
        biomass_id=1,
        price_per_kg_avg=Decimal("2.50")
    )
    assert price.biomass_id == 1
    assert price.price_per_kg_avg == Decimal("2.50")


def test_field_sample_creation():
    """Test creating a FieldSample instance."""
    sample = FieldSample(
        biomass_id=1,
        sample_name="Sample-001",
        amount_collected_kg=Decimal("50.5")
    )
    assert sample.biomass_id == 1
    assert sample.sample_name == "Sample-001"
    assert sample.amount_collected_kg == Decimal("50.5")
    assert isinstance(sample.created_at, datetime)


def test_harvest_method_creation():
    """Test creating a HarvestMethod instance."""
    method = HarvestMethod(harvest_method_name="Manual")
    assert method.harvest_method_name == "Manual"


def test_collection_method_creation():
    """Test creating a CollectionMethod instance."""
    method = CollectionMethod(collection_method_name="Rake")
    assert method.collection_method_name == "Rake"


def test_field_storage_creation():
    """Test creating a FieldStorage instance."""
    storage = FieldStorage(storage_method="Silo")
    assert storage.storage_method == "Silo"


def test_biomass_persistence(session):
    """Test saving and retrieving a Biomass instance from database."""
    biomass = Biomass(biomass_name="Corn Stover")
    session.add(biomass)
    session.commit()
    session.refresh(biomass)

    assert biomass.biomass_id is not None

    retrieved = session.get(Biomass, biomass.biomass_id)
    assert retrieved is not None
    assert retrieved.biomass_name == "Corn Stover"


def test_primary_product_persistence(session):
    """Test saving and retrieving a PrimaryProduct instance from database."""
    product = PrimaryProduct(primary_product_name="Biodiesel")
    session.add(product)
    session.commit()
    session.refresh(product)

    assert product.primary_product_id is not None

    retrieved = session.get(PrimaryProduct, product.primary_product_id)
    assert retrieved is not None
    assert retrieved.primary_product_name == "Biodiesel"
