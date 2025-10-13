from __future__ import annotations

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Index


# ----------------------------------------------------------------------
# Data source / reference tables
# ----------------------------------------------------------------------


class DataSource(SQLModel, table=True):
    """Source of data (internal / external)."""
    __tablename__ = "data_sources"

    source_id: Optional[int] = Field(default=None, primary_key=True)
    source_name_id: Optional[int] = Field(default=None,
                                          description="Reference to source_names.source_name_id",
                                          foreign_key="source_names.source_name_id")
    source_type_id: Optional[int] = Field(default=None,
                                          description="Reference to source_types.source_type_id",
                                          foreign_key="source_types.source_type_id")
    data_resolution_id: Optional[int] = Field(default=None,
                                             description="Reference to location_resolutions.location_resolution_id",
                                             foreign_key="location_resolutions.location_resolution_id")
    description: Optional[str] = Field(default=None)
    url_id: Optional[int] = Field(default=None,
                                  description="Reference to url.url_id",
                                  foreign_key="url.url_id")
    import_timestamp: Optional[datetime] = Field(default=None)

    __table_args__ = (Index("idx_data_sources_source_name_id", "source_name_id"),)


class SourceName(SQLModel, table=True):
    """Human‑readable name for a data source."""
    __tablename__ = "source_names"

    source_name_id: Optional[int] = Field(default=None, primary_key=True)
    source_name: str = Field(..., unique=True, description="Not null")


class SourceType(SQLModel, table=True):
    """Type of source (e.g., internal, external)."""
    __tablename__ = "source_types"

    source_type_id: Optional[int] = Field(default=None, primary_key=True)
    source_type: str = Field(..., unique=True, description="Not null")


class Reference(SQLModel, table=True):
    """Bibliographic reference."""
    __tablename__ = "references"

    reference_id: Optional[int] = Field(default=None, primary_key=True)
    reference_title: Optional[str] = Field(default=None)
    reference_author: Optional[str] = Field(default=None)
    reference_publication: Optional[str] = Field(default=None)
    reference_date: Optional[date] = Field(default=None)
    reference_doi_id: Optional[int] = Field(default=None,
                                            description="Reference to DOI.doi_id",
                                            foreign_key="doi.doi_id")
    url_id: Optional[int] = Field(default=None,
                                   description="Reference to url.url_id",
                                   foreign_key="url.url_id")


class DOI(SQLModel, table=True):
    """Digital Object Identifier."""
    __tablename__ = "doi"

    doi_id: Optional[int] = Field(default=None, primary_key=True)
    doi: Optional[str] = Field(default=None)


class URL(SQLModel, table=True):
    """Unique URL."""
    __tablename__ = "url"

    url_id: Optional[int] = Field(default=None, primary_key=True)
    url: Optional[str] = Field(default=None, unique=True)
