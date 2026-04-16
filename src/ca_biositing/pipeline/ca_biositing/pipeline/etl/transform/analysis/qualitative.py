from __future__ import annotations

from decimal import Decimal, InvalidOperation
import re
from typing import Any, Dict, Optional

import pandas as pd
from prefect import get_run_logger, task

from ca_biositing.pipeline.utils.cleaning_functions import cleaning as cleaning_mod
from ca_biositing.pipeline.utils.cleaning_functions import coercion as coercion_mod
from ca_biositing.pipeline.utils.name_id_swap import normalize_dataframes


EXTRACT_SOURCES = ["data_source", "parameters", "use_case_enum", "qualitative_data"]

_RESOURCE_CANONICAL_MAP = {
    "almond hull": "almond hulls",
    "almond shell": "almond shells",
}


def _get_logger():
    try:
        return get_run_logger()
    except Exception:
        import logging

        return logging.getLogger(__name__)


def _first_existing_column(df: pd.DataFrame, candidates: list[str]) -> Optional[str]:
    for candidate in candidates:
        if candidate in df.columns:
            return candidate
    return None


def _normalize_db_name(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"[_-]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def _normalize_parameter_name(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"\s+", "_", text)
    return text


def _normalize_use_case_name(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def _canonicalize_resource_name(value: Any) -> Any:
    if value is None or pd.isna(value):
        return value
    text = str(value).strip().lower()
    text = re.sub(r"\s+", " ", text)
    return _RESOURCE_CANONICAL_MAP.get(text, text)


def _forward_fill_qualitative_columns(df: pd.DataFrame) -> pd.DataFrame:
    filled = df.copy()
    columns_to_fill = ["primary_ag_product", "resource", "storage_description", "transport_description"]
    columns_to_fill = [col for col in columns_to_fill if col in filled.columns]
    if not columns_to_fill:
        return filled

    block_anchor_columns = [col for col in ["primary_ag_product", "resource"] if col in filled.columns]
    if block_anchor_columns:
        block_starts = filled[block_anchor_columns].notna().any(axis=1).cumsum()
        for col in columns_to_fill:
            filled[col] = filled.groupby(block_starts, sort=False)[col].ffill()
    else:
        for col in columns_to_fill:
            filled[col] = filled[col].ffill()
    return filled


def _parse_bool(value: Any) -> Optional[bool]:
    if pd.isna(value):
        return None
    text = str(value).strip().lower()
    if text in {"true", "yes", "y", "1"}:
        return True
    if text in {"false", "no", "n", "0"}:
        return False
    return None


def _map_trend_to_numeric(value: Any) -> Optional[Decimal]:
    if value is None or pd.isna(value):
        return None
    text = str(value).strip().lower()
    if text in {"up", "increase", "increasing", "rising"}:
        return Decimal("1")
    if text in {"down", "decrease", "decreasing", "falling"}:
        return Decimal("-1")
    if text in {"steady", "stable", "flat", "no change"}:
        return Decimal("0")
    return None


def _to_decimal(value: str) -> Optional[Decimal]:
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return None


def _parse_decimal_token(raw_token: str) -> Optional[Decimal]:
    token = str(raw_token).strip()
    if token == "":
        return None

    token = token.replace(",", "").replace("$", "").replace("%", "").strip()
    if token == "":
        return None

    is_accounting_negative = token.startswith("(") and token.endswith(")")
    if is_accounting_negative:
        token = token[1:-1].strip()

    if token == "":
        return None

    if not re.fullmatch(r"[+-]?\d+(?:\.\d+)?", token):
        return None

    parsed = _to_decimal(token)
    if parsed is None:
        return None

    if is_accounting_negative and parsed > 0:
        return -parsed
    return parsed


def parse_decimal_range(raw: Any) -> tuple[Optional[Decimal], Optional[Decimal]]:
    if raw is None or pd.isna(raw):
        return None, None

    text = str(raw).strip()
    if text == "":
        return None, None

    compact_original = text.replace(",", "").replace(" ", "").lower()
    cleaned = text.replace(",", "").replace("$", "").strip()

    if compact_original == "($0-$40)" or cleaned.replace(" ", "").lower() == "(0-40)":
        return Decimal("-40"), Decimal("-10")

    normalized = cleaned.replace("–", "-").replace("—", "-")
    to_split = re.split(r"(?i)\bto\b", normalized)
    if len(to_split) == 2:
        low = _parse_decimal_token(to_split[0])
        high = _parse_decimal_token(to_split[1])
        if low is None or high is None:
            return None, None
        return (low, high) if low <= high else (high, low)

    dash_split = re.match(r"^\s*(.+?)\s*-\s*(.+?)\s*$", normalized)
    if dash_split:
        low = _parse_decimal_token(dash_split.group(1))
        high = _parse_decimal_token(dash_split.group(2))
        if low is None or high is None:
            return None, None
        return (low, high) if low <= high else (high, low)

    single = _parse_decimal_token(normalized)
    if single is None:
        return None, None
    return single, single


def _build_end_use_record_key(resource: Any, use_case: Any) -> str:
    resource_key = ""
    if resource is not None and not pd.isna(resource):
        resource_key = str(resource).strip().lower()

    use_case_key = ""
    if use_case is not None and not pd.isna(use_case):
        use_case_key = str(use_case).strip().lower()

    return f"{resource_key}|{use_case_key}"


@task
def transform_qualitative_data_source(
    data_sources: Dict[str, pd.DataFrame],
    etl_run_id: str | None = None,
    lineage_group_id: str | None = None,
) -> Optional[pd.DataFrame]:
    logger = _get_logger()
    if "data_source" not in data_sources:
        logger.error("Required data source 'data_source' not found.")
        return None

    df = data_sources["data_source"].copy()
    if df.empty:
        return pd.DataFrame()

    cleaned = cleaning_mod.standard_clean(df, lowercase=False)
    if cleaned is None:
        return pd.DataFrame()

    rename_map = {
        "source_name": "name",
        "author": "creator",
        "url": "uri",
    }
    cleaned = cleaned.rename(columns=rename_map)
    cleaned = coercion_mod.coerce_columns(cleaned, datetime_cols=["date"])
    if "biocirv" in cleaned.columns:
        cleaned["biocirv"] = cleaned["biocirv"].apply(_parse_bool)

    cleaned["etl_run_id"] = etl_run_id
    cleaned["lineage_group_id"] = lineage_group_id

    desired_columns = [
        "name",
        "description",
        "full_title",
        "creator",
        "subject",
        "publisher",
        "contributor",
        "date",
        "type",
        "biocirv",
        "format",
        "language",
        "relation",
        "temporal_coverage",
        "rights",
        "license",
        "uri",
        "note",
        "etl_run_id",
        "lineage_group_id",
    ]

    for col in desired_columns:
        if col not in cleaned.columns:
            cleaned[col] = pd.NA

    return cleaned[desired_columns].copy()


@task
def transform_qualitative_parameters(
    data_sources: Dict[str, pd.DataFrame],
    etl_run_id: str | None = None,
    lineage_group_id: str | None = None,
) -> Optional[pd.DataFrame]:
    logger = _get_logger()
    if "parameters" not in data_sources:
        logger.error("Required data source 'parameters' not found.")
        return None

    from ca_biositing.datamodels.models import Unit

    df = data_sources["parameters"].copy()
    if df.empty:
        return pd.DataFrame()

    cleaned = cleaning_mod.standard_clean(df)
    if cleaned is None:
        return pd.DataFrame()

    name_col = _first_existing_column(cleaned, ["name", "parameter", "parameter_name"])
    if name_col and name_col != "name":
        cleaned = cleaned.rename(columns={name_col: "name"})

    cleaned["name"] = cleaned["name"].apply(_normalize_parameter_name)

    if "calculated" in cleaned.columns:
        cleaned["calculated"] = cleaned["calculated"].apply(_parse_bool)
    else:
        cleaned["calculated"] = pd.NA

    unit_col = _first_existing_column(cleaned, ["standard_unit", "unit", "unit_name"])
    if unit_col and unit_col != "standard_unit":
        cleaned = cleaned.rename(columns={unit_col: "standard_unit"})

    normalize_columns = {"standard_unit": (Unit, "name")}
    normalized_df = normalize_dataframes(cleaned, normalize_columns)[0]
    if "standard_unit_id" not in normalized_df.columns:
        normalized_df["standard_unit_id"] = pd.NA

    normalized_df["parameter_dedupe_key"] = normalized_df["name"].astype(str).str.strip().str.lower()
    normalized_df["etl_run_id"] = etl_run_id
    normalized_df["lineage_group_id"] = lineage_group_id

    desired_columns = [
        "name",
        "description",
        "calculated",
        "standard_unit_id",
        "parameter_dedupe_key",
        "etl_run_id",
        "lineage_group_id",
    ]
    for col in desired_columns:
        if col not in normalized_df.columns:
            normalized_df[col] = pd.NA

    return normalized_df[desired_columns].copy()


@task
def transform_qualitative_use_case_enum(
    data_sources: Dict[str, pd.DataFrame],
    etl_run_id: str | None = None,
    lineage_group_id: str | None = None,
) -> Optional[pd.DataFrame]:
    logger = _get_logger()
    if "use_case_enum" not in data_sources:
        logger.error("Required data source 'use_case_enum' not found.")
        return None

    df = data_sources["use_case_enum"].copy()
    if df.empty:
        return pd.DataFrame()

    cleaned = cleaning_mod.standard_clean(df)
    if cleaned is None:
        return pd.DataFrame()

    use_case_name_col = _first_existing_column(cleaned, ["use_case_name"])
    if not use_case_name_col:
        logger.warning("Expected 'use_case_name' column not found in use_case_enum sheet.")
        return pd.DataFrame(columns=["name", "description", "use_case_dedupe_key", "etl_run_id", "lineage_group_id"])
    if use_case_name_col != "name":
        cleaned = cleaned.rename(columns={use_case_name_col: "name"})

    cleaned["name"] = cleaned["name"].apply(_normalize_use_case_name)
    cleaned = cleaned[cleaned["name"].astype(str).str.strip() != ""].copy()
    cleaned = cleaned.drop_duplicates(subset=["name"], keep="first")
    cleaned["use_case_dedupe_key"] = cleaned["name"].astype(str).str.strip().str.lower()
    cleaned["etl_run_id"] = etl_run_id
    cleaned["lineage_group_id"] = lineage_group_id

    desired_columns = [
        "name",
        "description",
        "use_case_dedupe_key",
        "etl_run_id",
        "lineage_group_id",
    ]
    for col in desired_columns:
        if col not in cleaned.columns:
            cleaned[col] = pd.NA

    return cleaned[desired_columns].copy()


@task
def transform_qualitative_provenance_payloads(
    etl_run_id: str | None = None,
    lineage_group_id: str | None = None,
) -> Dict[str, pd.DataFrame]:
    datasets_df = pd.DataFrame(
        [
            {
                "name": "qualitative data",
                "record_type": "resource_storage_record, resource_transport_record, resource_end_use_record",
                "source_id": pd.NA,
                "start_date": pd.to_datetime("2025-11-01").date(),
                "end_date": pd.to_datetime("2026-05-01").date(),
                "etl_run_id": etl_run_id,
                "lineage_group_id": lineage_group_id,
            }
        ]
    )

    method_category_df = pd.DataFrame(
        [
            {
                "name": "research method",
                "description": "methods used in research (i.e. survey, interview, literature review)",
                "uri": pd.NA,
            }
        ]
    )

    method_df = pd.DataFrame(
        [
            {
                "name": "BEAM Circular interviews with industry stakeholders",
                "method_abbrev_id": pd.NA,
                "method_category_name": "research method",
                "source_id": pd.NA,
                "etl_run_id": etl_run_id,
                "lineage_group_id": lineage_group_id,
            }
        ]
    )

    place_df = pd.DataFrame(
        [
            {
                "geoid": "NSJV",
                "state_name": "california",
                "state_fips": "06",
                "county_name": pd.NA,
                "county_fips": pd.NA,
                "agg_level_desc": "IN-STATE REGION",
            }
        ]
    )

    return {
        "dataset": datasets_df,
        "method_category": method_category_df,
        "method": method_df,
        "place": place_df,
    }


@task
def transform_qualitative_records(
    data_sources: Dict[str, pd.DataFrame],
    etl_run_id: str | None = None,
    lineage_group_id: str | None = None,
) -> Optional[Dict[str, pd.DataFrame]]:
    logger = _get_logger()
    if "qualitative_data" not in data_sources:
        logger.error("Required data source 'qualitative_data' not found.")
        return None

    from ca_biositing.datamodels.models import Resource, UseCase

    def _build_use_case_map() -> dict[str, str]:
        enum_df = data_sources.get("use_case_enum")
        if not isinstance(enum_df, pd.DataFrame) or enum_df.empty:
            return {}
        cleaned_enum = cleaning_mod.standard_clean(enum_df.copy())
        if cleaned_enum is None or cleaned_enum.empty:
            return {}
        original_col = _first_existing_column(
            cleaned_enum,
            [
                "original_set_of_unique_use_case_names",
                "original set of unique use case names",
                "original_use_case_name",
                "original_use_case",
                "use_case",
            ],
        )
        canonical_col = _first_existing_column(cleaned_enum, ["use_case_name"])
        if canonical_col is None:
            return {}
        mapping: dict[str, str] = {}
        for _, row in cleaned_enum.iterrows():
            canonical = _normalize_use_case_name(row.get(canonical_col))
            if canonical == "":
                continue
            mapping[canonical] = canonical
            if original_col:
                original = _normalize_use_case_name(row.get(original_col))
                if original:
                    mapping[original] = canonical
        return mapping

    raw_df = data_sources["qualitative_data"].copy()
    if raw_df.empty:
        return {
            "resource_storage_record": pd.DataFrame(),
            "resource_transport_record": pd.DataFrame(),
            "resource_end_use_record": pd.DataFrame(),
        }

    cleaned = cleaning_mod.standard_clean(raw_df)
    if cleaned is None:
        return {
            "resource_storage_record": pd.DataFrame(),
            "resource_transport_record": pd.DataFrame(),
            "resource_end_use_record": pd.DataFrame(),
        }

    resource_col = _first_existing_column(cleaned, ["resource", "resource_name"])
    use_case_col = _first_existing_column(cleaned, ["use_case_name", "use_case", "end_use"])
    storage_col = _first_existing_column(cleaned, ["storage_description", "storage", "storage_desc"])
    transport_col = _first_existing_column(cleaned, ["transport_description", "transport", "transport_desc"])

    if resource_col and resource_col != "resource":
        cleaned = cleaned.rename(columns={resource_col: "resource"})
    if use_case_col and use_case_col != "use_case":
        cleaned = cleaned.rename(columns={use_case_col: "use_case"})
    cleaned = _forward_fill_qualitative_columns(cleaned)
    if "resource" in cleaned.columns:
        cleaned["resource"] = cleaned["resource"].apply(_canonicalize_resource_name)

    use_case_map = _build_use_case_map()
    if use_case_map and "use_case" in cleaned.columns:
        cleaned["use_case"] = cleaned["use_case"].apply(lambda value: use_case_map.get(_normalize_use_case_name(value), _normalize_use_case_name(value)))
    cleaned["end_use_record_key"] = cleaned.apply(
        lambda row: _build_end_use_record_key(row.get("resource"), row.get("use_case")),
        axis=1,
    )
    if storage_col and storage_col != "storage_description":
        cleaned = cleaned.rename(columns={storage_col: "storage_description"})
    if transport_col and transport_col != "transport_description":
        cleaned = cleaned.rename(columns={transport_col: "transport_description"})

    normalize_columns = {
        "resource": (Resource, "name"),
        "use_case": (UseCase, "name"),
    }
    normalized = normalize_dataframes(cleaned, normalize_columns)[0]

    if "end_use_record_key" not in normalized.columns:
        normalized["end_use_record_key"] = normalized.apply(
            lambda row: _build_end_use_record_key(row.get("resource"), row.get("use_case")),
            axis=1,
        )
    normalized["etl_run_id"] = etl_run_id
    normalized["lineage_group_id"] = lineage_group_id

    if "storage_description" in normalized.columns:
        storage_df = normalized[normalized["storage_description"].notna()].copy()
    else:
        storage_df = pd.DataFrame()
    if not storage_df.empty:
        storage_df["dataset_id"] = pd.NA
        storage_df["method_id"] = pd.NA
        storage_df["geoid"] = pd.NA
        storage_df["source_id"] = pd.NA
        storage_df = storage_df[
            [
                "resource_id",
                "storage_description",
                "dataset_id",
                "method_id",
                "geoid",
                "source_id",
                "etl_run_id",
                "lineage_group_id",
            ]
        ]

    if "transport_description" in normalized.columns:
        transport_df = normalized[normalized["transport_description"].notna()].copy()
    else:
        transport_df = pd.DataFrame()
    if not transport_df.empty:
        transport_df["dataset_id"] = pd.NA
        transport_df["method_id"] = pd.NA
        transport_df["geoid"] = pd.NA
        transport_df["source_id"] = pd.NA
        transport_df = transport_df[
            [
                "resource_id",
                "transport_description",
                "dataset_id",
                "method_id",
                "geoid",
                "source_id",
                "etl_run_id",
                "lineage_group_id",
            ]
        ]

    end_use_df = normalized.copy()
    end_use_df["dataset_id"] = pd.NA
    end_use_df["method_id"] = pd.NA
    end_use_df["geoid"] = pd.NA
    end_use_df["source_id"] = pd.NA
    if "use_case_id" not in end_use_df.columns:
        end_use_df["use_case_id"] = pd.NA
    end_use_df = end_use_df[
        [
            "resource_id",
            "use_case_id",
            "dataset_id",
            "method_id",
            "geoid",
            "source_id",
            "end_use_record_key",
            "etl_run_id",
            "lineage_group_id",
        ]
    ]

    return {
        "resource_storage_record": storage_df if isinstance(storage_df, pd.DataFrame) else pd.DataFrame(),
        "resource_transport_record": transport_df if isinstance(transport_df, pd.DataFrame) else pd.DataFrame(),
        "resource_end_use_record": end_use_df,
    }


@task
def transform_qualitative_observations(
    data_sources: Dict[str, pd.DataFrame],
    etl_run_id: str | None = None,
    lineage_group_id: str | None = None,
) -> Optional[pd.DataFrame]:
    logger = _get_logger()
    if "qualitative_data" not in data_sources:
        logger.error("Required data source 'qualitative_data' not found.")
        return None

    from ca_biositing.datamodels.models import Parameter, Unit

    qualitative_df = cleaning_mod.standard_clean(data_sources["qualitative_data"].copy())
    parameters_df = cleaning_mod.standard_clean(data_sources.get("parameters", pd.DataFrame()).copy())

    if qualitative_df is None or qualitative_df.empty:
        return pd.DataFrame()

    resource_col = _first_existing_column(qualitative_df, ["resource", "resource_name"])
    use_case_col = _first_existing_column(qualitative_df, ["use_case_name", "use_case", "end_use"])
    if resource_col and resource_col != "resource":
        qualitative_df = qualitative_df.rename(columns={resource_col: "resource"})
    if use_case_col and use_case_col != "use_case":
        qualitative_df = qualitative_df.rename(columns={use_case_col: "use_case"})
    qualitative_df = _forward_fill_qualitative_columns(qualitative_df)
    if "resource" in qualitative_df.columns:
        qualitative_df["resource"] = qualitative_df["resource"].apply(_canonicalize_resource_name)

    use_case_map = {}
    enum_df = data_sources.get("use_case_enum")
    if isinstance(enum_df, pd.DataFrame) and not enum_df.empty:
        cleaned_enum = cleaning_mod.standard_clean(enum_df.copy())
        if cleaned_enum is not None and not cleaned_enum.empty:
            original_col = _first_existing_column(
                cleaned_enum,
                [
                    "original_set_of_unique_use_case_names",
                    "original set of unique use case names",
                    "original_use_case_name",
                    "original_use_case",
                    "use_case",
                ],
            )
            canonical_col = _first_existing_column(cleaned_enum, ["use_case_name"])
            if canonical_col is not None:
                for _, row in cleaned_enum.iterrows():
                    canonical = _normalize_use_case_name(row.get(canonical_col))
                    if canonical:
                        use_case_map[canonical] = canonical
                        if original_col:
                            original = _normalize_use_case_name(row.get(original_col))
                            if original:
                                use_case_map[original] = canonical
    if use_case_map and "use_case" in qualitative_df.columns:
        qualitative_df["use_case"] = qualitative_df["use_case"].apply(lambda value: use_case_map.get(_normalize_use_case_name(value), _normalize_use_case_name(value)))

    parameter_to_unit: dict[str, Any] = {}
    if parameters_df is not None and not parameters_df.empty:
        param_name_col = _first_existing_column(parameters_df, ["name", "parameter", "parameter_name"])
        unit_col = _first_existing_column(parameters_df, ["standard_unit", "unit", "unit_name"])
        if param_name_col and unit_col:
            for _, row in parameters_df.iterrows():
                name_value = row.get(param_name_col)
                unit_value = row.get(unit_col)
                if pd.notna(name_value):
                    parameter_to_unit[str(name_value).strip().lower()] = unit_value

    records: list[dict[str, Any]] = []
    for _, row in qualitative_df.iterrows():
        record_key = _build_end_use_record_key(row.get("resource"), row.get("use_case"))

        perc_low, perc_high = parse_decimal_range(row.get("resource_use_perc_range"))
        value_low, value_high = parse_decimal_range(row.get("resource_value_usd_per_ton_delivered_range"))
        mult_low, mult_high = parse_decimal_range(row.get("resource_value_multiplier"))
        trend_value = row.get("resource_use_trend")

        parsed_values = {
            "resource_use_perc_low": perc_low,
            "resource_use_perc_high": perc_high,
            "resource_value_low": value_low,
            "resource_value_high": value_high,
            "resource_value_multiplier_low": mult_low,
            "resource_value_multiplier_high": mult_high,
        }

        for parameter_name, numeric_value in parsed_values.items():
            if numeric_value is None:
                continue
            unit_name = parameter_to_unit.get(parameter_name)
            records.append(
                {
                    "end_use_record_key": record_key,
                    "record_type": "resource_end_use_record",
                    "record_id": pd.NA,
                    "parameter_name": parameter_name,
                    "parameter": parameter_name,
                    "unit": unit_name,
                    "value": numeric_value,
                    "note": pd.NA,
                }
            )

        if pd.notna(trend_value) and str(trend_value).strip() != "":
            unit_name = parameter_to_unit.get("resource_use_trend")
            trend_numeric = _map_trend_to_numeric(trend_value)
            records.append(
                {
                    "end_use_record_key": record_key,
                    "record_type": "resource_end_use_record",
                    "record_id": pd.NA,
                    "parameter_name": "resource_use_trend",
                    "parameter": "resource_use_trend",
                    "unit": unit_name,
                    "value": trend_numeric,
                    "note": str(trend_value),
                }
            )

    obs_df = pd.DataFrame(records)
    if obs_df.empty:
        return pd.DataFrame()

    normalize_columns = {
        "parameter": (Parameter, "name"),
        "unit": (Unit, "name"),
    }
    normalized_obs_df = normalize_dataframes(obs_df, normalize_columns)[0]
    normalized_obs_df = normalized_obs_df.rename(
        columns={"parameter_id": "parameter_id", "unit_id": "unit_id"}
    )

    normalized_obs_df["etl_run_id"] = etl_run_id
    normalized_obs_df["lineage_group_id"] = lineage_group_id
    desired_columns = [
        "end_use_record_key",
        "record_type",
        "record_id",
        "parameter_name",
        "parameter_id",
        "unit_id",
        "value",
        "note",
        "etl_run_id",
        "lineage_group_id",
    ]
    for col in desired_columns:
        if col not in normalized_obs_df.columns:
            normalized_obs_df[col] = pd.NA

    return normalized_obs_df[desired_columns].copy()


@task
def transform_qualitative_payloads(
    data_sources: Dict[str, pd.DataFrame],
    etl_run_id: str | None = None,
    lineage_group_id: str | None = None,
) -> Dict[str, Any]:
    return {
        "data_source": transform_qualitative_data_source.fn(
            data_sources=data_sources,
            etl_run_id=etl_run_id,
            lineage_group_id=lineage_group_id,
        ),
        "parameter": transform_qualitative_parameters.fn(
            data_sources=data_sources,
            etl_run_id=etl_run_id,
            lineage_group_id=lineage_group_id,
        ),
        "use_case": transform_qualitative_use_case_enum.fn(
            data_sources=data_sources,
            etl_run_id=etl_run_id,
            lineage_group_id=lineage_group_id,
        ),
        "provenance": transform_qualitative_provenance_payloads.fn(
            etl_run_id=etl_run_id,
            lineage_group_id=lineage_group_id,
        ),
        "records": transform_qualitative_records.fn(
            data_sources=data_sources,
            etl_run_id=etl_run_id,
            lineage_group_id=lineage_group_id,
        ),
        "observation": transform_qualitative_observations.fn(
            data_sources=data_sources,
            etl_run_id=etl_run_id,
            lineage_group_id=lineage_group_id,
        ),
    }
