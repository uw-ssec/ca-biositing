import pandas as pd
import pytest
from unittest.mock import MagicMock, patch
from ca_biositing.pipeline.etl.transform.field_sampling.field_sample import transform_field_sample
from sqlalchemy import Column, String, Integer

@patch("ca_biositing.pipeline.utils.engine.engine")
@patch("ca_biositing.pipeline.utils.name_id_swap.Session")
def test_transform_field_sample(mock_session, mock_engine):
    # 1. Setup Mock Data
    metadata_raw = pd.DataFrame({
        "Field_Sample_Name": ["Pos-Alf033", "Pos-Alf033"],
        "Resource": ["Alfalfa", "Alfalfa"],
        "Provider_codename": ["possessive", "possessive"],
        "FV_Date_Time": ["6/30/2025 10:30", "6/30/2025 10:30"],
        "Sample_TS": ["6/30/2025 10:45", "6/30/2025 10:45"],
        "Qty": ["1", "1"],
        "Primary_Collector": ["Ziad Nasef", "Xihui Kang"],
        "Sample_Notes": ["Note 1", "Note 2"],
        "Sample_Source": ["Source A", "Source B"],
        "Prepared_Sample": ["Sample A", "Sample B"],
        "Storage_Mode": ["Method A", "Method B"]
    })

    provider_raw = pd.DataFrame({
        "Provider_codename": ["possessive"],
        "County": ["San Joaquin"],
        "Primary_Ag_Product": ["Alfalfa"],
        "Provider_type": ["Farmer"],
        "Field_Storage_Location": ["Address A"]
    })

    data_sources = {
        "samplemetadata": metadata_raw,
        "provider_info": provider_raw
    }

    # 2. Mock DB responses for normalization
    mock_db = MagicMock()
    mock_session.return_value.__enter__.return_value = mock_db

    def mock_execute(query):
        mock_result = MagicMock()
        query_str = str(query).lower()

        if "resource" in query_str:
            mock_result.all.return_value = [("alfalfa", 1)]
        elif "provider" in query_str:
            if "type" in query_str:
                mock_result.all.return_value = [("farmer", 11)]
            else:
                mock_result.all.return_value = [("possessive", 10)]
        elif "contact" in query_str:
            mock_result.all.return_value = [("ziad nasef", 100), ("xihui kang", 101)]
        elif "dataset" in query_str:
            mock_result.all.return_value = [("biocirv", 500)]
        elif "location_address" in query_str:
            if "county" in query_str:
                mock_result.all.return_value = [("san joaquin", 1000)]
            else:
                mock_result.all.return_value = [("address a", 1001)]
        elif "primary_ag_product" in query_str:
            mock_result.all.return_value = [("alfalfa", 2000)]
        elif "prepared_sample" in query_str:
            mock_result.all.return_value = [("sample a", 3000), ("sample b", 3001)]
        elif "method" in query_str:
            mock_result.all.return_value = [("method a", 4000), ("method b", 4001)]
        else:
            mock_result.all.return_value = []
        return mock_result

    mock_db.execute.side_effect = mock_execute

    # 3. Run Transform
    # We need to mock the models to have real SQLAlchemy Column objects to satisfy normalize_dataframes
    with patch('ca_biositing.datamodels.schemas.generated.ca_biositing.Contact') as MockContact, \
         patch('ca_biositing.datamodels.schemas.generated.ca_biositing.LocationAddress') as MockLoc, \
         patch('ca_biositing.datamodels.schemas.generated.ca_biositing.Provider') as MockProv, \
         patch('ca_biositing.datamodels.schemas.generated.ca_biositing.Resource') as MockRes, \
         patch('ca_biositing.datamodels.schemas.generated.ca_biositing.PreparedSample') as MockPrep, \
         patch('ca_biositing.datamodels.schemas.generated.ca_biositing.Method') as MockMeth, \
         patch('ca_biositing.datamodels.schemas.generated.ca_biositing.Dataset') as MockDS, \
         patch('ca_biositing.datamodels.schemas.generated.ca_biositing.PrimaryAgProduct') as MockAg, \
         patch('ca_biositing.datamodels.schemas.generated.ca_biositing.SoilType') as MockSoil, \
         patch('ca_biositing.datamodels.schemas.generated.ca_biositing.Unit') as MockUnit:

        for m in [MockContact, MockLoc, MockProv, MockRes, MockPrep, MockMeth, MockDS, MockAg, MockSoil, MockUnit]:
            m.__table__ = MagicMock()
            pk_col = Column('id', Integer, primary_key=True)
            m.__table__.primary_key.columns = [pk_col]

        MockContact.name = Column('name', String)
        MockLoc.county = Column('county', String)
        MockLoc.full_address = Column('full_address', String)
        MockProv.type = Column('type', String)
        MockProv.codename = Column('codename', String)
        MockRes.name = Column('name', String)
        MockPrep.name = Column('name', String)
        MockMeth.name = Column('name', String)
        MockDS.name = Column('name', String)
        MockAg.name = Column('name', String)
        MockSoil.name = Column('name', String)
        MockUnit.name = Column('name', String)

        result_df = transform_field_sample.fn(data_sources, etl_run_id=123, lineage_group_id=456)

    # 4. Assertions
    assert result_df is not None
    assert not result_df.empty
    assert len(result_df) == 2

    # Check columns (using the rename_map names)
    assert "name" in result_df.columns
    assert "resource_id" in result_df.columns
    assert "provider_id" in result_df.columns
    assert "collector_id" in result_df.columns
    assert "sample_collection_source" in result_df.columns
    assert "collection_timestamp" in result_df.columns
    assert "dataset_id" in result_df.columns
    assert "etl_run_id" in result_df.columns

    # Check values
    row = result_df.iloc[0].to_dict()

    assert row["resource_id"] == 1
    assert row["provider_id"] == 10
    assert row["collector_id"] == 100
    assert row["dataset_id"] == 500
    assert row["etl_run_id"] == 123
    assert row["lineage_group_id"] == 456

if __name__ == "__main__":
    pytest.main([__file__])
