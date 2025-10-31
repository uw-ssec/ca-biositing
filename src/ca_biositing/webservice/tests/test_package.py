"""Tests for the ca_biositing.webservice package."""

import ca_biositing.webservice


def test_version():
    """Test that the package has a version attribute."""
    assert hasattr(ca_biositing.webservice, "__version__")
    assert isinstance(ca_biositing.webservice.__version__, str)
    assert len(ca_biositing.webservice.__version__) > 0


def test_imports():
    """Test that main modules can be imported."""
    from ca_biositing.webservice import main

    assert hasattr(main, "app")
