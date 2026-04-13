"""
mv_biomass_end_uses.py

End-use breakdown per resource from ResourceEndUseRecord observations.

Grain: One row per resource × use_case combination.

Required index:
    CREATE UNIQUE INDEX idx_mv_biomass_end_uses_resource_use_case ON data_portal.mv_biomass_end_uses (resource_id, use_case)
"""

from sqlalchemy import select, func, case, cast, String, Float, Text, literal

from ca_biositing.datamodels.models.resource_information.resource import Resource
from ca_biositing.datamodels.models.resource_information.resource_end_use_record import ResourceEndUseRecord
from ca_biositing.datamodels.models.methods_parameters_units.method import Method
from ca_biositing.datamodels.models.general_analysis.observation import Observation
from ca_biositing.datamodels.models.methods_parameters_units.parameter import Parameter
from ca_biositing.datamodels.models.methods_parameters_units.unit import Unit


# Aggregate observations by record_id for end-use data
end_use_obs = select(
    Observation.record_id,
    func.avg(
        case(
            (
                func.lower(Parameter.name).in_(
                    [
                        "percent of volume",
                        "percent_of_volume",
                        "percentage of volume",
                        "volume percent",
                    ]
                ),
                Observation.value,
            )
        )
    ).label("percent_of_volume"),
    func.max(
        case(
            (
                func.lower(Parameter.name).in_(
                    [
                        "percent of volume",
                        "percent_of_volume",
                        "percentage of volume",
                        "volume percent",
                    ]
                ),
                Unit.name,
            )
        )
    ).label("unit"),
    func.max(
        case(
            (
                func.lower(Parameter.name) == "trending",
                cast(Observation.value, String),
            )
        )
    ).label("trending"),
).select_from(Observation)\
 .join(Parameter, Observation.parameter_id == Parameter.id)\
 .outerjoin(Unit, Observation.unit_id == Unit.id)\
 .where(func.lower(Observation.record_type) == "resource_end_use_record")\
 .group_by(Observation.record_id).subquery()

mv_biomass_end_uses = select(
    ResourceEndUseRecord.resource_id,
    Resource.name.label("resource_name"),
    func.coalesce(Method.name, literal("unknown")).label("use_case"),
    cast(end_use_obs.c.percent_of_volume, Float).label("percentage_low"),
    cast(literal(None), Float).label("percentage_high"),
    cast(end_use_obs.c.trending, Text).label("trend"),
    cast(literal(None), Float).label("value_low_usd"),
    cast(literal(None), Float).label("value_high_usd"),
    cast(literal(None), Text).label("value_notes"),
).select_from(ResourceEndUseRecord)\
 .join(Resource, ResourceEndUseRecord.resource_id == Resource.id)\
 .outerjoin(Method, ResourceEndUseRecord.method_id == Method.id)\
 .outerjoin(end_use_obs, cast(ResourceEndUseRecord.id, String) == end_use_obs.c.record_id)\
 .where(ResourceEndUseRecord.resource_id.is_not(None))\
 .group_by(
    ResourceEndUseRecord.resource_id,
    Resource.name,
    func.coalesce(Method.name, literal("unknown")),
    end_use_obs.c.percent_of_volume,
    end_use_obs.c.trending,
 )
