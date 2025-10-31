"""Tests for datamodels package metadata."""

from ca_biositing.datamodels import __version__


def test_version():
    """Test that package version is defined."""
    assert __version__ == "0.1.0"


def test_package_imports():
    """Test that package can be imported."""
    import ca_biositing.datamodels
    assert ca_biositing.datamodels is not None
    assert hasattr(ca_biositing.datamodels, "__version__")
