"""Tests for lookup utility functions."""

import pandas as pd
from ca_biositing.datamodels.biomass import BiomassType
from ca_biositing.pipeline.utils.lookup_utils import (
    replace_id_with_name_df,
    replace_name_with_id_df,
)


def test_replace_id_with_name_df(session):
    """Test replacing ID column with name column."""
    # Create test data in the reference table
    biomass_type1 = BiomassType(biomass_type="Crop by-product")
    biomass_type2 = BiomassType(biomass_type="Wood residue")
    session.add(biomass_type1)
    session.add(biomass_type2)
    session.commit()
    session.refresh(biomass_type1)
    session.refresh(biomass_type2)

    # Create test DataFrame with IDs
    df = pd.DataFrame({
        "sample_name": ["Sample1", "Sample2"],
        "biomass_type_id": [biomass_type1.biomass_type_id, biomass_type2.biomass_type_id]
    })

    # Replace IDs with names
    result_df = replace_id_with_name_df(
        db=session,
        df=df,
        ref_model=BiomassType,
        id_column_name="biomass_type_id",
        name_column_name="biomass_type"
    )

    # Verify results
    assert "biomass_type" in result_df.columns
    assert "biomass_type_id" not in result_df.columns
    assert result_df.loc[0, "biomass_type"] == "Crop by-product"
    assert result_df.loc[1, "biomass_type"] == "Wood residue"


def test_replace_name_with_id_df_existing_names(session):
    """Test replacing name column with ID column for existing names."""
    # Create test data in the reference table
    biomass_type1 = BiomassType(biomass_type="Crop by-product")
    biomass_type2 = BiomassType(biomass_type="Wood residue")
    session.add(biomass_type1)
    session.add(biomass_type2)
    session.commit()
    session.refresh(biomass_type1)
    session.refresh(biomass_type2)

    # Create test DataFrame with names
    df = pd.DataFrame({
        "sample_name": ["Sample1", "Sample2"],
        "biomass_type": ["Crop by-product", "Wood residue"]
    })

    # Replace names with IDs
    result_df = replace_name_with_id_df(
        db=session,
        df=df,
        ref_model=BiomassType,
        name_column_name="biomass_type",
        id_column_name="biomass_type_id"
    )

    # Verify results
    assert "biomass_type_id" in result_df.columns
    assert "biomass_type" not in result_df.columns
    assert result_df.loc[0, "biomass_type_id"] == biomass_type1.biomass_type_id
    assert result_df.loc[1, "biomass_type_id"] == biomass_type2.biomass_type_id


def test_replace_name_with_id_df_new_names(session):
    """Test replacing name column with ID column, creating new entries."""
    # Create one existing biomass type
    biomass_type1 = BiomassType(biomass_type="Crop by-product")
    session.add(biomass_type1)
    session.commit()
    session.refresh(biomass_type1)

    # Create test DataFrame with one existing and one new name
    df = pd.DataFrame({
        "sample_name": ["Sample1", "Sample2"],
        "biomass_type": ["Crop by-product", "Algae"]
    })

    # Replace names with IDs (should create "Algae" entry)
    result_df = replace_name_with_id_df(
        db=session,
        df=df,
        ref_model=BiomassType,
        name_column_name="biomass_type",
        id_column_name="biomass_type_id"
    )

    # Verify results
    assert "biomass_type_id" in result_df.columns
    assert "biomass_type" not in result_df.columns
    assert result_df.loc[0, "biomass_type_id"] == biomass_type1.biomass_type_id

    # Verify new entry was created
    algae_type = session.query(BiomassType).filter(BiomassType.biomass_type == "Algae").first()
    assert algae_type is not None
    assert result_df.loc[1, "biomass_type_id"] == algae_type.biomass_type_id


def test_replace_name_with_id_df_preserves_other_columns(session):
    """Test that other DataFrame columns are preserved."""
    # Create test data
    biomass_type = BiomassType(biomass_type="Crop by-product")
    session.add(biomass_type)
    session.commit()
    session.refresh(biomass_type)

    # Create test DataFrame with multiple columns
    df = pd.DataFrame({
        "sample_name": ["Sample1"],
        "biomass_type": ["Crop by-product"],
        "amount": [100.5],
        "notes": ["Test note"]
    })

    # Replace names with IDs
    result_df = replace_name_with_id_df(
        db=session,
        df=df,
        ref_model=BiomassType,
        name_column_name="biomass_type",
        id_column_name="biomass_type_id"
    )

    # Verify other columns are preserved
    assert "sample_name" in result_df.columns
    assert "amount" in result_df.columns
    assert "notes" in result_df.columns
    assert result_df.loc[0, "sample_name"] == "Sample1"
    assert result_df.loc[0, "amount"] == 100.5
    assert result_df.loc[0, "notes"] == "Test note"
