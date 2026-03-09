from sqlalchemy import select, func, union_all, literal, case, cast, String, Integer, Numeric, Boolean, and_, or_, Text
from sqlalchemy.sql import expression
from ca_biositing.datamodels.models.resource_information.resource import Resource, ResourceClass, ResourceSubclass, ResourceMorphology
from ca_biositing.datamodels.models.resource_information.primary_ag_product import PrimaryAgProduct
from ca_biositing.datamodels.models.external_data.billion_ton import BillionTon2023Record
from ca_biositing.datamodels.models.general_analysis.observation import Observation
from ca_biositing.datamodels.models.methods_parameters_units.parameter import Parameter
from ca_biositing.datamodels.models.methods_parameters_units.unit import Unit
from ca_biositing.datamodels.models.places.place import Place
from ca_biositing.datamodels.models.resource_information.resource_availability import ResourceAvailability
from ca_biositing.datamodels.models.aim1_records.compositional_record import CompositionalRecord
from ca_biositing.datamodels.models.aim1_records.proximate_record import ProximateRecord
from ca_biositing.datamodels.models.aim1_records.ultimate_record import UltimateRecord
from ca_biositing.datamodels.models.aim1_records.xrf_record import XrfRecord
from ca_biositing.datamodels.models.aim1_records.icp_record import IcpRecord
from ca_biositing.datamodels.models.aim1_records.calorimetry_record import CalorimetryRecord
from ca_biositing.datamodels.models.aim2_records.fermentation_record import FermentationRecord
from ca_biositing.datamodels.models.aim2_records.strain import Strain
from ca_biositing.datamodels.models.aim2_records.gasification_record import GasificationRecord
from ca_biositing.datamodels.models.external_data.usda_survey import UsdaMarketRecord, UsdaMarketReport
from ca_biositing.datamodels.models.external_data.usda_census import UsdaCommodity
from ca_biositing.datamodels.models.places.location_address import LocationAddress

# 1. mv_biomass_search
# Aggregated volume from Billion Ton
agg_vol = select(
    BillionTon2023Record.resource_id,
    func.sum(BillionTon2023Record.production).label("total_annual_volume")
).group_by(BillionTon2023Record.resource_id).subquery()

mv_biomass_search = select(
    Resource.id,
    Resource.name,
    Resource.resource_code,
    Resource.description,
    ResourceClass.name.label("resource_class"),
    ResourceSubclass.name.label("resource_subclass"),
    PrimaryAgProduct.name.label("primary_product"),
    ResourceMorphology.morphology_uri.label("image_url"),
    agg_vol.c.total_annual_volume,
    # Placeholders for composition flags/metrics - can be expanded later
    literal(False).label("has_moisture_data"),
    literal(False).label("has_sugar_data")
).select_from(Resource)\
 .outerjoin(ResourceClass, Resource.resource_class_id == ResourceClass.id)\
 .outerjoin(ResourceSubclass, Resource.resource_subclass_id == ResourceSubclass.id)\
 .outerjoin(PrimaryAgProduct, Resource.primary_ag_product_id == PrimaryAgProduct.id)\
 .outerjoin(ResourceMorphology, ResourceMorphology.resource_id == Resource.id)\
 .outerjoin(agg_vol, agg_vol.c.resource_id == Resource.id)


# 2. mv_biomass_composition
def get_composition_query(model, analysis_type):
    return select(
        model.resource_id,
        literal(analysis_type).label("analysis_type"),
        Parameter.name.label("parameter_name"),
        Observation.value.label("value"),
        Unit.name.label("unit")
    ).join(Observation, Observation.record_id == model.record_id)\
     .join(Parameter, Observation.parameter_id == Parameter.id)\
     .outerjoin(Unit, Observation.unit_id == Unit.id)

comp_queries = [
    get_composition_query(CompositionalRecord, "compositional"),
    get_composition_query(ProximateRecord, "proximate"),
    get_composition_query(UltimateRecord, "ultimate"),
    get_composition_query(XrfRecord, "xrf"),
    get_composition_query(IcpRecord, "icp"),
    get_composition_query(CalorimetryRecord, "calorimetry")
]

all_measurements = union_all(*comp_queries).subquery()

mv_biomass_composition = select(
    all_measurements.c.resource_id,
    Resource.name.label("resource_name"),
    all_measurements.c.analysis_type,
    all_measurements.c.parameter_name,
    all_measurements.c.unit,
    func.avg(all_measurements.c.value).label("avg_value"),
    func.min(all_measurements.c.value).label("min_value"),
    func.max(all_measurements.c.value).label("max_value"),
    func.stddev(all_measurements.c.value).label("std_dev"),
    func.count().label("observation_count")
).select_from(all_measurements)\
 .join(Resource, all_measurements.c.resource_id == Resource.id)\
 .group_by(
    all_measurements.c.resource_id,
    Resource.name,
    all_measurements.c.analysis_type,
    all_measurements.c.parameter_name,
    all_measurements.c.unit
)


# 3. mv_biomass_county_production
mv_biomass_county_production = select(
    func.row_number().over().label("id"),
    BillionTon2023Record.resource_id,
    Resource.name.label("resource_name"),
    Place.geoid,
    Place.county_name.label("county"),
    Place.state_name.label("state"),
    BillionTon2023Record.scenario_name.label("scenario"),
    BillionTon2023Record.production,
    BillionTon2023Record.year_num.label("year") if hasattr(BillionTon2023Record, 'year_num') else literal(2023).label("year") # Assuming year field or static
).select_from(BillionTon2023Record)\
 .join(Resource, BillionTon2023Record.resource_id == Resource.id)\
 .join(Place, BillionTon2023Record.geoid == Place.geoid)


# 4. mv_biomass_availability
# Aggregating to one row per resource
mv_biomass_availability = select(
    Resource.id.label("resource_id"),
    Resource.name.label("resource_name"),
    func.min(ResourceAvailability.from_month).label("from_month"),
    func.max(ResourceAvailability.to_month).label("to_month"),
    func.bool_or(ResourceAvailability.year_round).label("year_round"),
    func.avg(ResourceAvailability.residue_factor_dry_tons_acre).label("avg_residue_factor_dry"),
    func.avg(ResourceAvailability.residue_factor_wet_tons_acre).label("avg_residue_factor_wet")
).select_from(ResourceAvailability)\
 .join(Resource, ResourceAvailability.resource_id == Resource.id)\
 .group_by(Resource.id, Resource.name)


# 5. mv_biomass_sample_stats
def get_sample_stats_query(model):
    return select(
        model.resource_id,
        model.prepared_sample_id,
        model.dataset_id
    )

sample_queries = [
    get_sample_stats_query(CompositionalRecord),
    get_sample_stats_query(ProximateRecord),
    get_sample_stats_query(UltimateRecord),
    get_sample_stats_query(XrfRecord),
    get_sample_stats_query(IcpRecord),
    get_sample_stats_query(CalorimetryRecord)
]

all_samples = union_all(*sample_queries).subquery()

mv_biomass_sample_stats = select(
    Resource.id.label("resource_id"),
    Resource.name.label("resource_name"),
    func.count(func.distinct(all_samples.c.prepared_sample_id)).label("sample_count"),
    func.count(func.distinct(all_samples.c.dataset_id)).label("dataset_count"),
    func.count().label("total_record_count")
).select_from(Resource)\
 .outerjoin(all_samples, all_samples.c.resource_id == Resource.id)\
 .group_by(Resource.id, Resource.name)


# 6. mv_biomass_fermentation
mv_biomass_fermentation = select(
    FermentationRecord.resource_id,
    Strain.name.label("strain_name"),
    Parameter.name.label("parameter_name"),
    func.avg(Observation.value).label("avg_value"),
    func.min(Observation.value).label("min_value"),
    func.max(Observation.value).label("max_value"),
    func.count().label("observation_count")
).select_from(FermentationRecord)\
 .join(Strain, FermentationRecord.strain_id == Strain.id)\
 .join(Observation, Observation.record_id == FermentationRecord.record_id)\
 .join(Parameter, Observation.parameter_id == Parameter.id)\
 .group_by(FermentationRecord.resource_id, Strain.name, Parameter.name)


# 7. mv_biomass_gasification
mv_biomass_gasification = select(
    GasificationRecord.resource_id,
    Parameter.name.label("parameter_name"),
    func.avg(Observation.value).label("avg_value"),
    func.min(Observation.value).label("min_value"),
    func.max(Observation.value).label("max_value"),
    func.count().label("observation_count")
).select_from(GasificationRecord)\
 .join(Observation, Observation.record_id == GasificationRecord.record_id)\
 .join(Parameter, Observation.parameter_id == Parameter.id)\
 .group_by(GasificationRecord.resource_id, Parameter.name)


# 8. mv_biomass_pricing
mv_biomass_pricing = select(
    func.row_number().over().label("id"),
    UsdaCommodity.name.label("commodity_name"),
    Place.county_name.label("county"),
    Place.state_name.label("state"),
    UsdaMarketRecord.report_date,
    UsdaMarketRecord.market_type_category,
    UsdaMarketRecord.sale_type,
    literal(0).label("price_min"),
    literal(0).label("price_max"),
    literal(0).label("price_avg")
).select_from(UsdaMarketRecord)\
 .join(UsdaMarketReport, UsdaMarketRecord.report_id == UsdaMarketReport.id)\
 .join(UsdaCommodity, UsdaMarketRecord.commodity_id == UsdaCommodity.id)\
 .outerjoin(LocationAddress, UsdaMarketReport.office_city_id == LocationAddress.id)\
 .outerjoin(Place, LocationAddress.geography_id == Place.geoid)
