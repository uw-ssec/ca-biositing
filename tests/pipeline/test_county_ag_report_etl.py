"""
Test suite for County Ag Report ETL pipeline (Phase 4).

Tests extract, transform, and load steps for county_ag_report workflow.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone


class TestCountyAgReportExtract:
    """Test the extract step for county ag reports."""

    def test_extract_module_exists(self):
        """Verify that the extract module can be imported."""
        from ca_biositing.pipeline.etl.extract import county_ag_report
        assert county_ag_report is not None
        assert hasattr(county_ag_report, 'primary_products')
        assert hasattr(county_ag_report, 'pp_production_value')
        assert hasattr(county_ag_report, 'pp_data_sources')

    def test_extract_has_correct_sheet_names(self):
        """Verify the extract module uses correct Google Sheet names."""
        from ca_biositing.pipeline.etl.extract import county_ag_report
        assert county_ag_report.GSHEET_NAME == "Aim 1-Feedstock Collection and Processing Data-BioCirV"


class TestCountyAgReportTransform:
    """Test the transform steps for county ag reports."""

    def test_transform_records_returns_dataframe(self):
        """Test that record transform returns a DataFrame with correct columns and record IDs."""
        from ca_biositing.pipeline.etl.transform.analysis import county_ag_report_record

        # Mock input data
        meta_data = pd.DataFrame({
            'Prod_Nbr': ['pc-001', 'pc-002'],
            'Primary_product': ['Almonds', 'Walnuts'],
            'Produced_NSJV': ['Yes', 'No'],
            'Processed_NSJV': ['Yes', 'Yes'],
        })

        metrics_data = pd.DataFrame({
            'Prod_Nbr': ['pc-001', 'pc-001'],
            'Data_Year': [2023, 2024],
            'Prodn_Merced': [100, 110],
            'Value_$M_Merced': [50, 55],
            'Prodn_Value_note': ['Note 1', 'Note 2']
        })

        with patch('ca_biositing.pipeline.etl.transform.analysis.county_ag_report_record.normalize_dataframes') as mock_normalize:
            # Create a normalized DataFrame
            normalized_df = pd.DataFrame({
                'record_id': ['pc-001-merced-2023', 'pc-001-merced-2024'],
                'geoid': ['06047', '06047'],
                'primary_ag_product_id': [1, 1],
                'data_year': [2023, 2024],
                'data_source_id': [1, 5],
                'produced_nsjv': [True, True],
                'processed_nsjv': [True, True],
            })
            mock_normalize.return_value = [normalized_df]

            result = county_ag_report_record.transform_county_ag_report_records.fn(
                data_sources={
                    "primary_products": meta_data,
                    "pp_production_value": metrics_data
                },
                etl_run_id="test-run",
                lineage_group_id=1
            )

            assert result is not None
            assert not result.empty
            assert 'record_id' in result.columns
            assert result.iloc[0]['record_id'] == 'pc-001-merced-2023'
            assert bool(result.iloc[0]['produced_nsjv']) is True

    def test_transform_observations_returns_dataframe(self):
        """Test that observation transform correctly melts wide data."""
        from ca_biositing.pipeline.etl.transform.analysis import county_ag_report_observation

        metrics_data = pd.DataFrame({
            'Prod_Nbr': ['pc-001'],
            'Data_Year': [2023],
            'Prodn_Merced': [100],
            'Value_$M_Merced': [50],
        })

        with patch('ca_biositing.pipeline.etl.transform.analysis.county_ag_report_observation.normalize_dataframes') as mock_normalize:
            # Resulting melted data should have 2 observations (production and value)
            normalized_df = pd.DataFrame({
                'record_id': ['pc-001-merced-2023', 'pc-001-merced-2023'],
                'parameter_id': [79, 80],
                'unit_id': [1, 2],
                'value': [100.0, 50.0],
            })
            mock_normalize.return_value = [normalized_df]

            # Mock database lookup for datasets
            with patch('ca_biositing.pipeline.utils.engine.get_engine'):
                with patch('sqlalchemy.text'):
                    result = county_ag_report_observation.transform_county_ag_report_observations.fn(
                        data_sources={"pp_production_value": metrics_data},
                        etl_run_id="test-run",
                        lineage_group_id=1
                    )

            assert result is not None
            assert len(result) == 2
            assert 'record_id' in result.columns
            assert 'value' in result.columns


class TestCountyAgReportLoad:
    """Test the load step for county ag reports."""

    @patch('ca_biositing.pipeline.utils.engine.get_engine')
    def test_load_records_calls_execute(self, mock_get_engine):
        """Verify load_county_ag_report_records calls database execution."""
        from ca_biositing.pipeline.etl.load.analysis import county_ag_report_record

        mock_session = MagicMock()
        mock_conn = MagicMock()
        mock_get_engine.return_value.connect.return_value.__enter__.return_value = mock_conn

        # Mock Session to work with 'with' statement
        with patch('ca_biositing.pipeline.etl.load.analysis.county_ag_report_record.Session', return_value=mock_session):
            df = pd.DataFrame({
                'record_id': ['test-1'],
                'geoid': ['06047'],
                'data_year': [2023]
            })

            county_ag_report_record.load_county_ag_report_records.fn(df)

            assert mock_session.__enter__.return_value.execute.called
            assert mock_session.__enter__.return_value.commit.called


class TestCountyAgReportFlow:
    """Test the Prefect flow for county ag reports."""

    def test_flow_imports_correctly(self):
        """Verify the flow can be imported and has the correct name."""
        from ca_biositing.pipeline.flows.county_ag_report_etl import county_ag_report_flow
        assert county_ag_report_flow.name == "County Ag Report ETL"
