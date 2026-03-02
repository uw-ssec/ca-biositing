"""Shared USDA commodity lookup helpers for census and survey services."""

from __future__ import annotations

from typing import Optional

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from ca_biositing.datamodels.models import UsdaCommodity
from ca_biositing.webservice.exceptions import CropNotFoundException


def normalize_crop_name(crop_name: Optional[str]) -> str:
    """Normalize crop names for case- and space-insensitive exact matching."""
    if not crop_name:
        return ""
    return " ".join(crop_name.split()).lower()


def normalized_sql_text(column):
    """Normalize SQL text for case- and space-insensitive exact matching.

    Three replace passes collapse whitespace runs up to 8 spaces while keeping
    SQLite compatibility in tests.
    """
    normalized = column
    for _ in range(3):
        normalized = func.replace(normalized, "  ", " ")
    return func.lower(func.trim(normalized))


def get_commodity_by_name(session: Session, crop_name: str) -> UsdaCommodity:
    """Get USDA commodity by crop name, preferring api_name over name matches."""
    normalized_query = normalize_crop_name(crop_name)

    api_name_match = UsdaCommodity.api_name.is_not(None) & (
        normalized_sql_text(UsdaCommodity.api_name) == normalized_query
    )
    name_match = UsdaCommodity.name.is_not(None) & (
        normalized_sql_text(UsdaCommodity.name) == normalized_query
    )

    stmt = (
        select(UsdaCommodity)
        .where(api_name_match | name_match)
        .order_by(
            case((api_name_match, 0), else_=1),
            UsdaCommodity.id,
        )
        .limit(1)
    )
    commodity = session.execute(stmt).scalar_one_or_none()
    if commodity is None:
        raise CropNotFoundException(crop_name)

    return commodity
