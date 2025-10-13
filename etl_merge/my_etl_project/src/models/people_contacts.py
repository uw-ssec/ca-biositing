from __future__ import annotations

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Index

# ----------------------------------------------------------------------
# People / contacts
# ----------------------------------------------------------------------


class AnalystContact(SQLModel, table=True):
    """Analyst or data‑entry contact."""
    __tablename__ = "analysts_contacts"

    analyst_id: Optional[int] = Field(default=None, primary_key=True)
    analyst_first_name: Optional[str] = Field(default=None)
    analyst_last_name: Optional[str] = Field(default=None)
    analyst_email: Optional[str] = Field(default=None)
    analyst_affiliation: Optional[int] = Field(default=None,
                                               description="Reference to affiliations.affiliation_id",
                                               foreign_key="affiliations.affiliation_id")


class Provider(SQLModel, table=True):
    """Provider of samples / data."""
    __tablename__ = "providers"

    provider_id: Optional[int] = Field(default=None, primary_key=True)
    provider_name: str = Field(..., unique=True, description="Not null")
    provider_affiliation: Optional[int] = Field(default=None,
                                                description="Reference to affiliations.affiliation_id",
                                                foreign_key="affiliations.affiliation_id")
    provider_type_id: Optional[int] = Field(default=None,
                                            description="Reference to provider_types.provider_type_id",
                                            foreign_key="provider_types.provider_type_id")
    anonymous: Optional[bool] = Field(default=None)


class ProviderType(SQLModel, table=True):
    """Category of provider (facility, farm, processor, etc.)."""
    __tablename__ = "provider_types"

    provider_type_id: Optional[int] = Field(default=None, primary_key=True)
    provider_type: Optional[str] = Field(default=None)


class Collector(SQLModel, table=True):
    """Collector of field samples."""
    __tablename__ = "collectors"

    collector_id: Optional[int] = Field(default=None, primary_key=True)
    collector_name: str = Field(..., unique=True, description="Not null")
    collector_affiliation: Optional[int] = Field(default=None,
                                                 description="Reference to affiliations.affiliation_id",
                                                 foreign_key="affiliations.affiliation_id")
