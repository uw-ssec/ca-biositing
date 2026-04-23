from __future__ import annotations

import argparse
import io
import subprocess
from typing import Optional

import pandas as pd


def _run_sql(sql: str) -> pd.DataFrame:
    cmd = [
        "docker-compose",
        "-f",
        "resources/docker/docker-compose.yml",
        "exec",
        "-T",
        "db",
        "psql",
        "-U",
        "biocirv_user",
        "-d",
        "biocirv_db",
        "-X",
        "-A",
        "-F",
        "\t",
        "-P",
        "footer=off",
        "-c",
        sql,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Failed to execute SQL via docker-compose psql")

    output = result.stdout.strip()
    if output == "":
        return pd.DataFrame()

    return pd.read_csv(io.StringIO(output), sep="\t")


def _print_section(title: str, df: pd.DataFrame) -> None:
    print(f"\n=== {title} ===")
    if df.empty:
        print("(no rows)")
        return
    print(df.to_string(index=False))


def query_observations_with_names(parameter_id: Optional[int], parameter_name: Optional[str], limit: int) -> pd.DataFrame:
    parameter_filter = ""
    if parameter_id is not None:
        parameter_filter = f"AND o.parameter_id = {int(parameter_id)}"

    parameter_name_filter = ""
    if parameter_name is not None and parameter_name.strip() != "":
        safe_name = parameter_name.strip().replace("'", "''")
        parameter_name_filter = f"AND lower(p.name) = lower('{safe_name}')"

    sql = f"""
        SELECT
            o.id AS observation_id,
            o.record_id AS end_use_record_id,
            r.id AS resource_id,
            r.name AS resource_name,
            uc.id AS use_case_id,
            uc.name AS use_case_name,
            p.id AS parameter_id,
            p.name AS parameter_name,
            u.id AS unit_id,
            u.name AS unit_name,
            o.value AS numeric_value,
            o.note AS text_note,
            CASE
                WHEN o.value IS NOT NULL THEN o.value::text
                ELSE o.note
            END AS resolved_value,
            CASE
                WHEN o.value IS NOT NULL THEN 'numeric'
                ELSE 'text'
            END AS value_source,
            CASE
                WHEN p.name = 'resource_use_trend' THEN
                    CASE
                        WHEN lower(trim(coalesce(o.note, ''))) IN ('up', 'increase', 'increasing', 'rising') THEN 1
                        WHEN lower(trim(coalesce(o.note, ''))) IN ('down', 'decrease', 'decreasing', 'falling') THEN -1
                        WHEN lower(trim(coalesce(o.note, ''))) IN ('steady', 'stable', 'flat', 'no change') THEN 0
                        ELSE NULL
                    END
                ELSE NULL
            END AS trend_code
        FROM observation o
        JOIN resource_end_use_record eur
            ON eur.id::text = o.record_id
           AND o.record_type = 'resource_end_use_record'
        LEFT JOIN resource r ON r.id = eur.resource_id
        LEFT JOIN use_case uc ON uc.id = eur.use_case_id
        LEFT JOIN parameter p ON p.id = o.parameter_id
        LEFT JOIN unit u ON u.id = o.unit_id
        WHERE 1 = 1
          {parameter_filter}
                    {parameter_name_filter}
        ORDER BY o.id
        LIMIT {int(limit)}
    """
    return _run_sql(sql)


def query_first_rows_per_parameter(
    first_n: int,
    parameter_id: Optional[int] = None,
    parameter_name: Optional[str] = None,
) -> pd.DataFrame:
    parameter_filter = ""
    if parameter_id is not None:
        parameter_filter = f"AND o.parameter_id = {int(parameter_id)}"

    parameter_name_filter = ""
    if parameter_name is not None and parameter_name.strip() != "":
        safe_name = parameter_name.strip().replace("'", "''")
        parameter_name_filter = f"AND lower(p.name) = lower('{safe_name}')"

    sql = f"""
        WITH base AS (
            SELECT
                o.id AS observation_id,
                o.record_id AS end_use_record_id,
                r.id AS resource_id,
                r.name AS resource_name,
                uc.id AS use_case_id,
                uc.name AS use_case_name,
                p.id AS parameter_id,
                p.name AS parameter_name,
                u.id AS unit_id,
                u.name AS unit_name,
                o.value AS numeric_value,
                o.note AS text_note,
                CASE
                    WHEN o.value IS NOT NULL THEN o.value::text
                    ELSE o.note
                END AS resolved_value,
                CASE
                    WHEN o.value IS NOT NULL THEN 'numeric'
                    ELSE 'text'
                END AS value_source,
                CASE
                    WHEN p.name = 'resource_use_trend' THEN
                        CASE
                            WHEN lower(trim(coalesce(o.note, ''))) IN ('up', 'increase', 'increasing', 'rising') THEN 1
                            WHEN lower(trim(coalesce(o.note, ''))) IN ('down', 'decrease', 'decreasing', 'falling') THEN -1
                            WHEN lower(trim(coalesce(o.note, ''))) IN ('steady', 'stable', 'flat', 'no change') THEN 0
                            ELSE NULL
                        END
                    ELSE NULL
                END AS trend_code
            FROM observation o
            JOIN resource_end_use_record eur
                ON eur.id::text = o.record_id
               AND o.record_type = 'resource_end_use_record'
            LEFT JOIN resource r ON r.id = eur.resource_id
            LEFT JOIN use_case uc ON uc.id = eur.use_case_id
            LEFT JOIN parameter p ON p.id = o.parameter_id
            LEFT JOIN unit u ON u.id = o.unit_id
            WHERE 1 = 1
              {parameter_filter}
              {parameter_name_filter}
        ), ranked AS (
            SELECT
                base.*,
                ROW_NUMBER() OVER (PARTITION BY base.parameter_name ORDER BY base.observation_id) AS parameter_row_num
            FROM base
        )
        SELECT
            parameter_name,
            parameter_row_num,
            observation_id,
            end_use_record_id,
            resource_name,
            use_case_name,
            parameter_id,
            unit_id,
            unit_name,
            numeric_value,
            text_note,
            resolved_value,
            value_source,
            trend_code
        FROM ranked
        WHERE parameter_row_num <= {int(first_n)}
        ORDER BY parameter_name, parameter_row_num
    """
    return _run_sql(sql)


def query_almond_storage_transport() -> pd.DataFrame:
    sql = """
        SELECT
            t.table_name,
            t.record_id,
            t.resource_id,
            r.name AS resource_name,
            t.description
        FROM (
            SELECT
                'resource_storage_record'::text AS table_name,
                rsr.id AS record_id,
                rsr.resource_id,
                rsr.storage_description AS description
            FROM resource_storage_record rsr

            UNION ALL

            SELECT
                'resource_transport_record'::text AS table_name,
                rtr.id AS record_id,
                rtr.resource_id,
                rtr.transport_description AS description
            FROM resource_transport_record rtr
        ) t
        LEFT JOIN resource r ON r.id = t.resource_id
        WHERE lower(coalesce(r.name, '')) LIKE '%almond hull%'
           OR lower(coalesce(r.name, '')) LIKE '%almond shell%'
           OR t.resource_id IN (118, 119)
        ORDER BY t.table_name, t.record_id
    """
    return _run_sql(sql)


def query_use_case_reference_status() -> pd.DataFrame:
    sql = """
        SELECT
            uc.id,
            uc.name,
            COUNT(eur.id) AS end_use_reference_count
        FROM use_case uc
        LEFT JOIN resource_end_use_record eur ON eur.use_case_id = uc.id
        GROUP BY uc.id, uc.name
        ORDER BY end_use_reference_count DESC, uc.name
    """
    return _run_sql(sql)


def query_parameter_name_style() -> pd.DataFrame:
    sql = """
        SELECT
            id,
            name,
            CASE
                WHEN name = lower(name) AND name !~ '[A-Z]' THEN 'lowercase_or_snake_case'
                ELSE 'mixed_or_upper_case'
            END AS style_check
        FROM parameter
        WHERE name IN (
            'resource_use_perc_low',
            'resource_use_perc_high',
            'resource_value_low',
            'resource_value_high',
            'resource_value_multiplier_low',
            'resource_value_multiplier_high',
            'resource_use_trend'
        )
        ORDER BY id
    """
    return _run_sql(sql)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit qualitative ETL foreign-key references with human-readable names."
    )
    parser.add_argument(
        "--parameter-id",
        type=int,
        default=None,
        help="Optional filter for observation.parameter_id (example: 2).",
    )
    parser.add_argument(
        "--parameter-name",
        type=str,
        default=None,
        help="Optional filter for parameter name (example: resource_use_trend).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=200,
        help="Row limit for observation join output.",
    )
    parser.add_argument(
        "--first-n-per-parameter",
        type=int,
        default=5,
        help="How many rows to show for each parameter in grouped end-use snapshot.",
    )
    args = parser.parse_args()

    obs_df = query_observations_with_names(args.parameter_id, args.parameter_name, args.limit)
    first_per_param_df = query_first_rows_per_parameter(
        first_n=args.first_n_per_parameter,
        parameter_id=args.parameter_id,
        parameter_name=args.parameter_name,
    )
    almond_df = query_almond_storage_transport()
    use_case_df = query_use_case_reference_status()
    parameter_style_df = query_parameter_name_style()

    _print_section("Observation joined to end-use/resource/use-case/parameter/unit (numeric_value vs text_note)", obs_df)
    _print_section(f"First {args.first_n_per_parameter} rows per parameter for resource_end_use_record", first_per_param_df)
    _print_section("Almond-related storage/transport records (includes resource_id 118/119)", almond_df)
    _print_section("Use-case reference counts from resource_end_use_record", use_case_df)
    _print_section("Qualitative parameter naming style check", parameter_style_df)


if __name__ == "__main__":
    main()
