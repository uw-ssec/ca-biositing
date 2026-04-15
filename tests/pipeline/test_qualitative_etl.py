"""Tests for Stage 2 qualitative ETL extract layer."""

from unittest.mock import patch

import pandas as pd


class TestQualitativeExtract:
    """Test the extract step for qualitative profile data."""

    def test_extract_module_exists(self):
        """Verify that the extract module can be imported."""
        from ca_biositing.pipeline.etl.extract import qualitative

        assert qualitative is not None
        assert hasattr(qualitative, "data_source")
        assert hasattr(qualitative, "parameters")
        assert hasattr(qualitative, "use_case_enum")
        assert hasattr(qualitative, "qualitative_data")
        assert hasattr(qualitative, "extract_qualitative_sheets")

    def test_extract_has_correct_sheet_names(self):
        """Verify the extract module uses the expected sheet names."""
        from ca_biositing.pipeline.etl.extract import qualitative

        assert qualitative.GSHEET_NAME == "1Hip4BfzqJFQmPctYKtSskRvIS_rGnEzd8zxYTGYYJ-c"
        assert qualitative.DATA_SOURCE_WORKSHEET == "data_source"
        assert qualitative.PARAMETERS_WORKSHEET == "parameters"
        assert qualitative.USE_CASE_ENUM_WORKSHEET == "use_case_enum"
        assert qualitative.QUALITATIVE_DATA_WORKSHEET == "qualitative_data"

    def test_extract_qualitative_sheets_returns_dict(self):
        """Verify the combined extract task returns keyed raw dataframes."""
        from ca_biositing.pipeline.etl.extract import qualitative

        data_source_df = pd.DataFrame({"name": ["source"]})
        parameters_df = pd.DataFrame({"name": ["parameter"]})
        use_case_df = pd.DataFrame({"use_case": ["fuel"]})
        qualitative_df = pd.DataFrame({"resource": ["almond hulls"]})

        with patch.object(qualitative.data_source, "fn", return_value=data_source_df), patch.object(
            qualitative.parameters, "fn", return_value=parameters_df
        ), patch.object(qualitative.use_case_enum, "fn", return_value=use_case_df), patch.object(
            qualitative.qualitative_data, "fn", return_value=qualitative_df
        ):
            result = qualitative.extract_qualitative_sheets.fn()

        assert isinstance(result, dict)
        assert set(result.keys()) == {"data_source", "parameters", "use_case_enum", "qualitative_data"}
        assert result["data_source"].equals(data_source_df)
        assert result["parameters"].equals(parameters_df)
        assert result["use_case_enum"].equals(use_case_df)
        assert result["qualitative_data"].equals(qualitative_df)
