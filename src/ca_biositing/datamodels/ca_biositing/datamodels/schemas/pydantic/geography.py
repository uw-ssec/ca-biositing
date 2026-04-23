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
     'description': 'Common geographic identifiers used across multiple datasets. '
                    'Includes states, counties, FIPS codes, and optional '
                    'regions.\n',
     'id': 'geography',
     'imports': ['linkml:types'],
     'name': 'Geography',
     'prefixes': {'agrovoc': {'prefix_prefix': 'agrovoc',
                              'prefix_reference': 'https://agrovoc.fao.org/agrontology/en/page/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'usda': {'prefix_prefix': 'usda',
                           'prefix_reference': 'https://schema.myorg.org/usda/'}},
     'source_file': 'schemas/common/geography.yaml'} )


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


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Geography.model_rebuild()
