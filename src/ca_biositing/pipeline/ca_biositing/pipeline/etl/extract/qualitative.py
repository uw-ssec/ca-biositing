"""ETL Extract: Qualitative profile data."""

from typing import Optional

import pandas as pd
from prefect import task

from .factory import create_extractor

GSHEET_NAME = "1Hip4BfzqJFQmPctYKtSskRvIS_rGnEzd8zxYTGYYJ-c"

DATA_SOURCE_WORKSHEET = "data_source"
PARAMETERS_WORKSHEET = "parameters"
USE_CASE_ENUM_WORKSHEET = "use_case_enum"
QUALITATIVE_DATA_WORKSHEET = "qualitative_data"

data_source = create_extractor(GSHEET_NAME, DATA_SOURCE_WORKSHEET)
parameters = create_extractor(GSHEET_NAME, PARAMETERS_WORKSHEET)
use_case_enum = create_extractor(GSHEET_NAME, USE_CASE_ENUM_WORKSHEET)
qualitative_data = create_extractor(GSHEET_NAME, QUALITATIVE_DATA_WORKSHEET)


@task(name="extract_qualitative_sheets")
def extract_qualitative_sheets(project_root: Optional[str] = None) -> dict[str, pd.DataFrame]:
    """Extract all qualitative ETL sheets and return them keyed by sheet purpose."""
    return {
        "data_source": data_source.fn(project_root=project_root),
        "parameters": parameters.fn(project_root=project_root),
        "use_case_enum": use_case_enum.fn(project_root=project_root),
        "qualitative_data": qualitative_data.fn(project_root=project_root),
    }
