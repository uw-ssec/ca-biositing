"""Tests for Stage 2 qualitative Prompt B transform layer."""

from unittest.mock import patch

import pandas as pd


class TestQualitativeTransform:
    """Targeted tests for qualitative transform functions."""

    def test_transform_module_exists(self):
        from ca_biositing.pipeline.etl.transform.analysis import qualitative

        assert qualitative is not None
        assert hasattr(qualitative, "transform_qualitative_data_source")
        assert hasattr(qualitative, "transform_qualitative_parameters")
        assert hasattr(qualitative, "transform_qualitative_use_case_enum")
        assert hasattr(qualitative, "transform_qualitative_records")
        assert hasattr(qualitative, "transform_qualitative_observations")

    def test_parse_decimal_range_parenthetical_negative(self):
        from ca_biositing.pipeline.etl.transform.analysis.qualitative import parse_decimal_range

        low, high = parse_decimal_range("($10)")
        assert str(low) == "-10"
        assert str(high) == "-10"

    def test_parse_decimal_range_special_rule(self):
        from ca_biositing.pipeline.etl.transform.analysis.qualitative import parse_decimal_range

        low, high = parse_decimal_range("($0-$40)")
        assert str(low) == "-40"
        assert str(high) == "-10"

    def test_parse_decimal_range_percent_positive_bounds(self):
        from ca_biositing.pipeline.etl.transform.analysis.qualitative import parse_decimal_range

        low, high = parse_decimal_range("50-70%")
        assert str(low) == "50"
        assert str(high) == "70"

    def test_parse_decimal_range_percent_with_spaces(self):
        from ca_biositing.pipeline.etl.transform.analysis.qualitative import parse_decimal_range

        low, high = parse_decimal_range("50 - 70 %")
        assert str(low) == "50"
        assert str(high) == "70"

    def test_transform_parameters_maps_bool_and_dedupe(self):
        from ca_biositing.pipeline.etl.transform.analysis import qualitative

        raw = pd.DataFrame(
            {
                "name": ["resource_use_perc_low", "resource_use_trend"],
                "calculated": ["Yes", "no"],
                "standard_unit": ["percent", "text"],
                "description": ["low range", "trend"],
            }
        )

        def mock_normalize(df, _normalize_columns):
            out = df.copy()
            out["standard_unit_id"] = [1, 2]
            return [out]

        with patch(
            "ca_biositing.pipeline.etl.transform.analysis.qualitative.normalize_dataframes",
            side_effect=mock_normalize,
        ):
            result = qualitative.transform_qualitative_parameters.fn({"parameters": raw}, "run-1", 9)

        assert isinstance(result, pd.DataFrame)
        assert list(result["calculated"]) == [True, False]
        assert "parameter_dedupe_key" in result.columns
        assert result.iloc[0]["name"] == "resource_use_perc_low"
        assert result.iloc[0]["parameter_dedupe_key"] == "resource_use_perc_low"
        assert result.iloc[0]["standard_unit_id"] == 1

    def test_transform_use_case_uses_canonical_name_column(self):
        from ca_biositing.pipeline.etl.transform.analysis import qualitative

        raw = pd.DataFrame(
            {
                "original set of unique use case names": ["Feed"],
                "use_case_name": ["Animal Feed"],
                "description": ["Used as feed"],
            }
        )

        result = qualitative.transform_qualitative_use_case_enum.fn({"use_case_enum": raw}, "run-1", 9)

        assert isinstance(result, pd.DataFrame)
        assert list(result["name"]) == ["animal feed"]

    def test_transform_use_case_requires_use_case_name_column(self):
        from ca_biositing.pipeline.etl.transform.analysis import qualitative

        raw = pd.DataFrame(
            {
                "use_case": ["Feed"],
                "description": ["Used as feed"],
            }
        )

        result = qualitative.transform_qualitative_use_case_enum.fn({"use_case_enum": raw}, "run-1", 9)

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_transform_records_emits_use_case_id_and_keys(self):
        from ca_biositing.pipeline.etl.transform.analysis import qualitative

        raw = pd.DataFrame(
            {
                "resource": ["almond hulls"],
                "use_case": ["animal feed"],
                "storage_description": ["covered pile"],
                "transport_description": ["truck"],
            }
        )

        def mock_normalize(df, _normalize_columns):
            out = df.copy()
            out["resource_id"] = [11]
            out["use_case_id"] = [5]
            return [out]

        with patch(
            "ca_biositing.pipeline.etl.transform.analysis.qualitative.normalize_dataframes",
            side_effect=mock_normalize,
        ):
            result = qualitative.transform_qualitative_records.fn({"qualitative_data": raw}, "run-1", 9)

        assert isinstance(result, dict)
        end_use_df = result["resource_end_use_record"]
        assert "use_case_id" in end_use_df.columns
        assert end_use_df.iloc[0]["use_case_id"] == 5
        assert end_use_df.iloc[0]["end_use_record_key"] == "almond hulls|animal feed"

    def test_transform_records_forward_fills_and_canonicalizes_resource(self):
        from ca_biositing.pipeline.etl.transform.analysis import qualitative

        raw = pd.DataFrame(
            {
                "primary_ag_product": ["Almond", pd.NA],
                "resource": ["Almond Hull", pd.NA],
                "use_case": ["animal feed", "bioenergy/cogeneration"],
                "storage_description": ["covered pile", pd.NA],
                "transport_description": ["truck", pd.NA],
            }
        )

        def mock_normalize(df, _normalize_columns):
            assert list(df["resource"]) == ["almond hulls", "almond hulls"]
            out = df.copy()
            out["resource_id"] = [11, 11]
            out["use_case_id"] = [5, 6]
            return [out]

        with patch(
            "ca_biositing.pipeline.etl.transform.analysis.qualitative.normalize_dataframes",
            side_effect=mock_normalize,
        ):
            result = qualitative.transform_qualitative_records.fn({"qualitative_data": raw}, "run-1", 9)

        end_use_df = result["resource_end_use_record"]
        assert len(end_use_df) == 2
        assert end_use_df.iloc[0]["end_use_record_key"] == "almond hulls|animal feed"
        assert end_use_df.iloc[1]["end_use_record_key"] == "almond hulls|bioenergy/cogeneration"

    def test_transform_records_preserves_key_when_normalize_drops_name_columns(self):
        from ca_biositing.pipeline.etl.transform.analysis import qualitative

        raw = pd.DataFrame(
            {
                "resource": ["almond hulls"],
                "use_case": ["animal feed"],
                "storage_description": ["covered pile"],
                "transport_description": ["truck"],
            }
        )

        def mock_normalize(df, _normalize_columns):
            out = df.copy()
            out = out.drop(columns=["resource", "use_case"])
            out["resource_id"] = [11]
            out["use_case_id"] = [5]
            return [out]

        with patch(
            "ca_biositing.pipeline.etl.transform.analysis.qualitative.normalize_dataframes",
            side_effect=mock_normalize,
        ):
            result = qualitative.transform_qualitative_records.fn({"qualitative_data": raw}, "run-1", 9)

        end_use_df = result["resource_end_use_record"]
        assert end_use_df.iloc[0]["end_use_record_key"] == "almond hulls|animal feed"

    def test_transform_records_maps_original_use_case_to_canonical(self):
        from ca_biositing.pipeline.etl.transform.analysis import qualitative

        qualitative_raw = pd.DataFrame(
            {
                "resource": ["Almond Hull"],
                "use_case": ["Bioenergy/cogeneration"],
                "storage_description": ["covered pile"],
                "transport_description": ["truck"],
            }
        )
        enum_raw = pd.DataFrame(
            {
                "original_set_of_unique_use_case_names": ["Bioenergy/cogeneration"],
                "use_case_name": ["Onsite Compined Heat and Power (CHP)"],
                "description": ["Alias mapping"],
            }
        )

        def mock_normalize(df, _normalize_columns):
            assert list(df["use_case"]) == ["onsite compined heat and power (chp)"]
            out = df.copy()
            out["resource_id"] = [9]
            out["use_case_id"] = [16]
            return [out]

        with patch(
            "ca_biositing.pipeline.etl.transform.analysis.qualitative.normalize_dataframes",
            side_effect=mock_normalize,
        ):
            result = qualitative.transform_qualitative_records.fn(
                {"qualitative_data": qualitative_raw, "use_case_enum": enum_raw},
                "run-1",
                9,
            )

        end_use_df = result["resource_end_use_record"]
        assert end_use_df.iloc[0]["end_use_record_key"] == "almond hulls|onsite compined heat and power (chp)"

    def test_transform_observations_parses_ranges_and_trend(self):
        from ca_biositing.pipeline.etl.transform.analysis import qualitative

        qualitative_df = pd.DataFrame(
            {
                "resource": ["almond hulls"],
                "use_case": ["animal feed"],
                "resource_use_perc_range": ["10-20"],
                "resource_value_usd_per_ton_delivered_range": ["($0-$40)"],
                "resource_value_multiplier": ["1.2-1.8"],
                "resource_use_trend": ["increasing"],
            }
        )
        parameters_df = pd.DataFrame(
            {
                "name": [
                    "resource_use_perc_low",
                    "resource_use_perc_high",
                    "resource_value_low",
                    "resource_value_high",
                    "resource_value_multiplier_low",
                    "resource_value_multiplier_high",
                    "resource_use_trend",
                ],
                "standard_unit": ["percent", "percent", "usd/ton", "usd/ton", "multiplier", "multiplier", "text"],
            }
        )

        def mock_normalize(df, _normalize_columns):
            out = df.copy()
            out["parameter_id"] = range(1, len(out) + 1)
            out["unit_id"] = range(101, 101 + len(out))
            return [out]

        with patch(
            "ca_biositing.pipeline.etl.transform.analysis.qualitative.normalize_dataframes",
            side_effect=mock_normalize,
        ):
            result = qualitative.transform_qualitative_observations.fn(
                {"qualitative_data": qualitative_df, "parameters": parameters_df},
                "run-1",
                9,
            )

        assert isinstance(result, pd.DataFrame)
        assert "end_use_record_key" in result.columns
        assert result["end_use_record_key"].iloc[0] == "almond hulls|animal feed"
        assert len(result) >= 7
        trend_rows = result[result["parameter_name"] == "resource_use_trend"]
        assert not trend_rows.empty
        assert str(trend_rows.iloc[0]["value"]) == "1"


class TestQualitativeSchemaFix:
    """Targeted tests for the interim schema model fix needed by Prompt B."""

    def test_use_case_model_exists(self):
        from ca_biositing.datamodels.models import UseCase

        assert UseCase.__tablename__ == "use_case"

    def test_resource_end_use_record_has_use_case_id(self):
        from ca_biositing.datamodels.models import ResourceEndUseRecord

        assert hasattr(ResourceEndUseRecord, "use_case_id")
        field_info = ResourceEndUseRecord.model_fields.get("use_case_id")
        assert field_info is not None
