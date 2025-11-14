from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )

    @model_serializer(mode='wrap', when_used='unless-none')
    def treat_empty_lists_as_none(
            self, handler: SerializerFunctionWrapHandler,
            info: SerializationInfo) -> dict[str, Any]:
        if info.exclude_none:
            _instance = self.model_copy()
            for field, field_info in type(_instance).model_fields.items():
                if getattr(_instance, field) == [] and not(
                        field_info.is_required()):
                    setattr(_instance, field, None)
        else:
            _instance = self
        return handler(_instance, info)



class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'usda',
     'description': 'Schema for USDA Census and Survey data records accessed via '
                    'the NASS Quick Stats API, focusing on county-level data for '
                    'key California crops.\n',
     'id': 'usda_data',
     'imports': ['linkml:types', '../common/geography'],
     'name': 'USDA_Data',
     'prefixes': {'agrovoc': {'prefix_prefix': 'agrovoc',
                              'prefix_reference': 'https://agrovoc.fao.org/agrontology/en/page/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'ucum': {'prefix_prefix': 'ucum',
                           'prefix_reference': 'http://unitsofmeasure.org/ucum.html'},
                  'usda': {'prefix_prefix': 'usda',
                           'prefix_reference': 'https://schema.myorg.org/usda/'}},
     'source_file': 'schemas/usda/census_survey.yaml'} )

class CropEnum(str, Enum):
    Almond = "Almond"
    """
    TODO: AGROVOC c_330
    """
    Pistachio = "Pistachio"
    """
    TODO: AGROVOC c_5733
    """
    Tomato = "Tomato"
    """
    TODO: AGROVOC c_7824
    """
    Olive = "Olive"
    """
    TODO: AGROVOC c_5681
    """


class VariableEnum(str, Enum):
    ACREAGE_TOTAL = "ACREAGE_TOTAL"
    """
    TODO: AGROVOC mapping
    """
    ACREAGE_BEARING = "ACREAGE_BEARING"
    """
    TODO: AGROVOC mapping
    """
    ACREAGE_NONBEARING = "ACREAGE_NONBEARING"
    """
    TODO: AGROVOC mapping
    """
    YIELD = "YIELD"
    """
    TODO: AGROVOC mapping
    """
    PRODUCTION = "PRODUCTION"
    """
    TODO: AGROVOC mapping
    """
    OPERATIONS = "OPERATIONS"
    """
    TODO: AGROVOC mapping
    """


class UnitEnum(str, Enum):
    ACRES = "ACRES"
    """
    TODO: UCUM mapping
    """
    TONS = "TONS"
    """
    TODO: UCUM mapping
    """
    TONS_PER_ACRE = "TONS_PER_ACRE"
    """
    TODO: UCUM mapping
    """
    OPERATIONS = "OPERATIONS"
    """
    TODO: AGROVOC or UCUM mapping
    """


class BearingStatusEnum(str, Enum):
    BEARING = "BEARING"
    """
    TODO: AGROVOC mapping
    """
    NONBEARING = "NONBEARING"
    """
    TODO: AGROVOC mapping
    """
    NA = "NA"
    """
    TODO: not applicable
    """



class Geography(ConfiguredBaseModel):
    """
    Reference table for U.S. geographic identifiers.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'geography'})

    state_name: Optional[str] = Field(default=None, description="""U.S. state name.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Geography']} })
    state_fips: Optional[str] = Field(default=None, description="""Two-digit FIPS code for the state.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Geography']} })
    county_name: Optional[str] = Field(default=None, description="""U.S. county name.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Geography']} })
    county_fips: Optional[str] = Field(default=None, description="""Three-digit county FIPS code.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Geography']} })
    geoid: Optional[str] = Field(default=None, description="""Combined state + county FIPS (e.g., 06019).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Geography']} })
    region_name: Optional[str] = Field(default=None, description="""Optional higher-level region grouping (e.g., San Joaquin Valley).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Geography']} })
    agg_level_desc: Optional[str] = Field(default=None, description="""Aggregation level (e.g., COUNTY, STATE, NATIONAL).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Geography']} })

    @field_validator('state_fips')
    def pattern_state_fips(cls, v):
        pattern=re.compile(r"^[0-9]{2}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid state_fips format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid state_fips format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('county_fips')
    def pattern_county_fips(cls, v):
        pattern=re.compile(r"^[0-9]{3}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid county_fips format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid county_fips format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('geoid')
    def pattern_geoid(cls, v):
        pattern=re.compile(r"^[0-9]{5}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid geoid format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid geoid format: {v}"
            raise ValueError(err_msg)
        return v


class USDARecord(ConfiguredBaseModel):
    """
    Base class for USDA agricultural data records.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'usda_data',
         'slot_usage': {'bearing_status': {'name': 'bearing_status',
                                           'range': 'BearingStatusEnum'},
                        'crop': {'name': 'crop', 'range': 'CropEnum'},
                        'geography': {'name': 'geography', 'range': 'Geography'},
                        'unit': {'name': 'unit', 'range': 'UnitEnum'},
                        'variable': {'name': 'variable', 'range': 'VariableEnum'}}})

    year: int = Field(default=..., description="""Census or survey year.""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    geography: Optional[Geography] = Field(default=None, description="""Geographic information (state, county, FIPS).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    crop: Optional[CropEnum] = Field(default=None, description="""Commodity or crop name.""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    variable: Optional[VariableEnum] = Field(default=None, description="""Census or survey variable measured (e.g., Acreage, Yield, Production).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    unit: Optional[UnitEnum] = Field(default=None, description="""Unit of measure (e.g., acres, tons, tons per acre).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    value: Optional[float] = Field(default=None, description="""Reported numeric value.""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    bearing_status: Optional[BearingStatusEnum] = Field(default=None, description="""Bearing or nonbearing acreage (if applicable).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    class_desc: Optional[str] = Field(default=None, description="""Class description (e.g., BEARING, NONBEARING).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    domain_desc: Optional[str] = Field(default=None, description="""Domain category (e.g., TOTAL, CHEMICAL, AREA HARVESTED).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    source: Optional[str] = Field(default=None, description="""Data source citation (e.g., USDA NASS Quick Stats API).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    notes: Optional[str] = Field(default=None, description="""Supplemental notes or flags (e.g., (D) data suppressed).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })


class CensusRecord(USDARecord):
    """
    A USDA Census of Agriculture record (every 5 years).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'usda_data'})

    year: int = Field(default=..., description="""Census or survey year.""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    geography: Optional[Geography] = Field(default=None, description="""Geographic information (state, county, FIPS).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    crop: Optional[CropEnum] = Field(default=None, description="""Commodity or crop name.""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    variable: Optional[VariableEnum] = Field(default=None, description="""Census or survey variable measured (e.g., Acreage, Yield, Production).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    unit: Optional[UnitEnum] = Field(default=None, description="""Unit of measure (e.g., acres, tons, tons per acre).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    value: Optional[float] = Field(default=None, description="""Reported numeric value.""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    bearing_status: Optional[BearingStatusEnum] = Field(default=None, description="""Bearing or nonbearing acreage (if applicable).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    class_desc: Optional[str] = Field(default=None, description="""Class description (e.g., BEARING, NONBEARING).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    domain_desc: Optional[str] = Field(default=None, description="""Domain category (e.g., TOTAL, CHEMICAL, AREA HARVESTED).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    source: Optional[str] = Field(default=None, description="""Data source citation (e.g., USDA NASS Quick Stats API).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    notes: Optional[str] = Field(default=None, description="""Supplemental notes or flags (e.g., (D) data suppressed).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })


class SurveyRecord(USDARecord):
    """
    A USDA Survey record (annual, seasonal, or periodic).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'usda_data'})

    period_desc: Optional[str] = Field(default=None, description="""For surveys, the time period of data collection (e.g., ANNUAL, MARCH).""", json_schema_extra = { "linkml_meta": {'domain_of': ['SurveyRecord']} })
    freq_desc: Optional[str] = Field(default=None, description="""For surveys, the frequency of data collection (e.g., ANNUAL, MONTHLY).""", json_schema_extra = { "linkml_meta": {'domain_of': ['SurveyRecord']} })
    program_desc: Optional[str] = Field(default=None, description="""Survey program name (e.g., FRUIT & TREE NUTS, VEGETABLES).""", json_schema_extra = { "linkml_meta": {'domain_of': ['SurveyRecord']} })
    year: int = Field(default=..., description="""Census or survey year.""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    geography: Optional[Geography] = Field(default=None, description="""Geographic information (state, county, FIPS).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    crop: Optional[CropEnum] = Field(default=None, description="""Commodity or crop name.""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    variable: Optional[VariableEnum] = Field(default=None, description="""Census or survey variable measured (e.g., Acreage, Yield, Production).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    unit: Optional[UnitEnum] = Field(default=None, description="""Unit of measure (e.g., acres, tons, tons per acre).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    value: Optional[float] = Field(default=None, description="""Reported numeric value.""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    bearing_status: Optional[BearingStatusEnum] = Field(default=None, description="""Bearing or nonbearing acreage (if applicable).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    class_desc: Optional[str] = Field(default=None, description="""Class description (e.g., BEARING, NONBEARING).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    domain_desc: Optional[str] = Field(default=None, description="""Domain category (e.g., TOTAL, CHEMICAL, AREA HARVESTED).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    source: Optional[str] = Field(default=None, description="""Data source citation (e.g., USDA NASS Quick Stats API).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })
    notes: Optional[str] = Field(default=None, description="""Supplemental notes or flags (e.g., (D) data suppressed).""", json_schema_extra = { "linkml_meta": {'domain_of': ['USDARecord']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Geography.model_rebuild()
USDARecord.model_rebuild()
CensusRecord.model_rebuild()
SurveyRecord.model_rebuild()
