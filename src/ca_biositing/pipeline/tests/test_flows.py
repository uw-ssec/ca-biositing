"""Tests for Prefect flows."""


def test_primary_product_flow_import():
    """Test that primary_product_flow can be imported."""
    from ca_biositing.pipeline.flows.primary_product import primary_product_flow
    assert primary_product_flow is not None
    assert callable(primary_product_flow)


def test_analysis_type_flow_import():
    """Test that analysis_type_flow can be imported."""
    from ca_biositing.pipeline.flows.analysis_type import analysis_type_flow
    assert analysis_type_flow is not None
    assert callable(analysis_type_flow)
