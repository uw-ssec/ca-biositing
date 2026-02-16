from ..base import BaseEntity, LookupBase
from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class UsdaMarketReport(BaseEntity, table=True):
    __tablename__ = "usda_market_report"

    slug_id: Optional[int] = Field(default=None)
    slug_name: Optional[str] = Field(default=None)
    report_series_title: Optional[str] = Field(default=None)
    frequency: Optional[str] = Field(default=None)
    office_name: Optional[str] = Field(default=None)
    office_city_id: Optional[int] = Field(default=None, foreign_key="location_address.id")
    office_state_fips: Optional[str] = Field(default=None)
    source_id: Optional[int] = Field(default=None, foreign_key="data_source.id")

    # Relationships
    office_city: Optional["LocationAddress"] = Relationship()
    source: Optional["DataSource"] = Relationship()


class UsdaMarketRecord(BaseEntity, table=True):
    __tablename__ = "usda_market_record"

    report_id: Optional[int] = Field(default=None, foreign_key="usda_market_report.id")
    dataset_id: Optional[int] = Field(default=None, foreign_key="dataset.id")
    report_begin_date: Optional[datetime] = Field(default=None)
    report_end_date: Optional[datetime] = Field(default=None)
    report_date: Optional[datetime] = Field(default=None)
    commodity_id: Optional[int] = Field(default=None, foreign_key="usda_commodity.id")
    market_type_id: Optional[int] = Field(default=None)
    market_type_category: Optional[str] = Field(default=None)
    grp: Optional[str] = Field(default=None)
    market_category_id: Optional[int] = Field(default=None)
    class_: Optional[str] = Field(default=None)
    grade: Optional[str] = Field(default=None)
    variety: Optional[str] = Field(default=None)
    protein_pct: Optional[Decimal] = Field(default=None)
    application: Optional[str] = Field(default=None)
    pkg: Optional[str] = Field(default=None)
    sale_type: Optional[str] = Field(default=None)
    price_unit_id: Optional[int] = Field(default=None, foreign_key="unit.id")
    freight: Optional[str] = Field(default=None)
    trans_mode: Optional[str] = Field(default=None)

    # Relationships
    report: Optional["UsdaMarketReport"] = Relationship()
    dataset: Optional["Dataset"] = Relationship()
    commodity: Optional["UsdaCommodity"] = Relationship()
    price_unit: Optional["Unit"] = Relationship()


class UsdaSurveyProgram(LookupBase, table=True):
    __tablename__ = "usda_survey_program"



class UsdaSurveyRecord(BaseEntity, table=True):
    __tablename__ = "usda_survey_record"

    dataset_id: Optional[int] = Field(default=None, foreign_key="dataset.id")
    geoid: Optional[str] = Field(default=None, foreign_key="place.geoid")
    commodity_code: Optional[int] = Field(default=None, foreign_key="usda_commodity.id")
    year: Optional[int] = Field(default=None)
    survey_program_id: Optional[int] = Field(default=None, foreign_key="usda_survey_program.id")
    survey_period: Optional[str] = Field(default=None)
    reference_month: Optional[str] = Field(default=None)
    begin_code: Optional[int] = Field(default=None)
    end_code: Optional[int] = Field(default=None)
    seasonal_flag: Optional[bool] = Field(default=None)
    note: Optional[str] = Field(default=None)

    # Relationships
    dataset: Optional["Dataset"] = Relationship()
    place: Optional["Place"] = Relationship()
    commodity: Optional["UsdaCommodity"] = Relationship()
    survey_program: Optional["UsdaSurveyProgram"] = Relationship()


class UsdaTermMap(BaseEntity, table=True):
    __tablename__ = "usda_term_map"

    source_system: Optional[str] = Field(default=None)
    source_context: Optional[str] = Field(default=None)
    raw_term: Optional[str] = Field(default=None)
    usda_commodity_id: Optional[int] = Field(default=None, foreign_key="usda_commodity.id")
    is_verified: Optional[bool] = Field(default=None)
    note: Optional[str] = Field(default=None)

    # Relationships
    usda_commodity: Optional["UsdaCommodity"] = Relationship()
