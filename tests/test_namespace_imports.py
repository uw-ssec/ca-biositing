"""Test namespace package imports."""

from __future__ import annotations


def test_datamodels_import():
    """Test that datamodels package can be imported."""
    from ca_biositing import datamodels

    assert datamodels.__version__ == "0.1.0"


def test_pipeline_import():
    """Test that pipeline package can be imported."""
    from ca_biositing import pipeline

    assert pipeline.__version__ == "0.1.0"


def test_model_imports():
    """Test that models can be imported from datamodels."""
    from ca_biositing.datamodels.models import FieldSample, PrimaryAgProduct
    from ca_biositing.datamodels.models import AnalysisType

    assert FieldSample.__tablename__ == "field_sample"
    assert PrimaryAgProduct.__tablename__ == "primary_ag_product"
    assert AnalysisType.__tablename__ == "analysis_type"


def test_database_import():
    """Test that database module can be imported."""
    from ca_biositing.datamodels import database

    assert hasattr(database, 'get_engine')
    assert hasattr(database, 'get_session')


def test_pipeline_flows_import():
    """Test that pipeline flows can be imported."""
    from ca_biositing.pipeline.flows.primary_ag_product import primary_ag_product_flow
    from ca_biositing.pipeline.flows.analysis_type import analysis_type_flow

    assert callable(primary_ag_product_flow)
    assert callable(analysis_type_flow)
