"""Tests for pipeline package metadata."""

from ca_biositing.pipeline import __version__


def test_version():
    """Test that package version is defined."""
    assert isinstance(__version__, str)
    assert __version__


def test_package_imports():
    """Test that package can be imported."""
    import ca_biositing.pipeline
    assert ca_biositing.pipeline is not None
    assert hasattr(ca_biositing.pipeline, "__version__")
