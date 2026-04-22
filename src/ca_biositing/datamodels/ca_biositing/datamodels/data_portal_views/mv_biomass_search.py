"""
mv_biomass_search.py

Comprehensive biomass search view combining resource metadata, analytical metrics,
availability data, and supply volume projections.

Required index:
    CREATE UNIQUE INDEX idx_mv_biomass_search_id ON data_portal.mv_biomass_search (id)
"""

from sqlalchemy import select, func, union_all, case, cast, String, Integer, Numeric, Boolean, and_, or_, Text, Float, ARRAY, text, true
from sqlalchemy.dialects.postgresql import array as pg_array
from sqlalchemy.orm import aliased

from ca_biositing.datamodels.models.resource_information.resource import Resource, ResourceClass, ResourceSubclass, ResourceMorphology
from ca_biositing.datamodels.models.resource_information.primary_ag_product import PrimaryAgProduct
from ca_biositing.datamodels.models.resource_information.resource_transport_record import ResourceTransportRecord
from ca_biositing.datamodels.models.resource_information.resource_storage_record import ResourceStorageRecord
from ca_biositing.datamodels.models.external_data.resource_usda_commodity_map import ResourceUsdaCommodityMap
from ca_biositing.datamodels.models.external_data.billion_ton import BillionTon2023Record
from ca_biositing.datamodels.models.general_analysis.observation import Observation
from ca_biositing.datamodels.models.methods_parameters_units.parameter import Parameter
from ca_biositing.datamodels.models.methods_parameters_units.unit import Unit
from ca_biositing.datamodels.models.aim1_records.compositional_record import CompositionalRecord
from ca_biositing.datamodels.models.aim1_records.proximate_record import ProximateRecord
from ca_biositing.datamodels.models.aim1_records.ultimate_record import UltimateRecord
from ca_biositing.datamodels.models.aim1_records.xrf_record import XrfRecord
from ca_biositing.datamodels.models.aim1_records.icp_record import IcpRecord
from ca_biositing.datamodels.models.aim1_records.calorimetry_record import CalorimetryRecord
from ca_biositing.datamodels.models.aim1_records.xrd_record import XrdRecord
from ca_biositing.datamodels.models.aim1_records.ftnir_record import FtnirRecord
from ca_biositing.datamodels.models.aim2_records.fermentation_record import FermentationRecord
from ca_biositing.datamodels.models.aim2_records.gasification_record import GasificationRecord
from ca_biositing.datamodels.models.aim2_records.pretreatment_record import PretreatmentRecord

from .common import analysis_metrics, resource_analysis_map, get_carbon_avg_expr, get_hydrogen_avg_expr, get_nitrogen_avg_expr, get_cn_ratio_expr


# Subquery for analytical averages (moisture, ash, lignin, sugar)
# Sugar = glucose + xylose
resource_metrics = select(
    resource_analysis_map.c.resource_id,
    func.avg(case((analysis_metrics.c.parameter == "moisture", analysis_metrics.c.value))).label("moisture_percent"),
    func.avg(case((analysis_metrics.c.parameter == "ash", analysis_metrics.c.value))).label("ash_percent"),
    # Lignin content = sum of averages of lignin and lignin+
    # Returns NULL if neither parameter is present for the resource
    case(
        (
            or_(
                func.avg(case((analysis_metrics.c.parameter == "lignin", analysis_metrics.c.value))).is_not(None),
                func.avg(case((analysis_metrics.c.parameter == "lignin+", analysis_metrics.c.value))).is_not(None)
            ),
            func.coalesce(func.avg(case((analysis_metrics.c.parameter == "lignin", analysis_metrics.c.value))), 0) +
            func.coalesce(func.avg(case((analysis_metrics.c.parameter == "lignin+", analysis_metrics.c.value))), 0)
        ),
        else_=None
    ).label("lignin_percent"),
    # Sugar content = sum of averages of glucose and xylose
    # Returns NULL if neither parameter is present for the resource
    case(
        (
            or_(
                func.avg(case((analysis_metrics.c.parameter == "glucose", analysis_metrics.c.value))).is_not(None),
                func.avg(case((analysis_metrics.c.parameter == "xylose", analysis_metrics.c.value))).is_not(None)
            ),
            func.coalesce(func.avg(case((analysis_metrics.c.parameter == "glucose", analysis_metrics.c.value))), 0) +
            func.coalesce(func.avg(case((analysis_metrics.c.parameter == "xylose", analysis_metrics.c.value))), 0)
        ),
        else_=None
    ).label("sugar_content_percent"),
    get_carbon_avg_expr().label("carbon_percent"),
    get_hydrogen_avg_expr().label("hydrogen_percent"),
    get_cn_ratio_expr().label("cn_ratio"),
    # Flags
    func.bool_or(resource_analysis_map.c.type == "proximate analysis").label("has_proximate"),
    func.bool_or(resource_analysis_map.c.type == "compositional analysis").label("has_compositional"),
    func.bool_or(resource_analysis_map.c.type == "ultimate analysis").label("has_ultimate"),
    func.bool_or(resource_analysis_map.c.type == "xrf analysis").label("has_xrf"),
    func.bool_or(resource_analysis_map.c.type == "icp analysis").label("has_icp"),
    func.bool_or(resource_analysis_map.c.type == "calorimetry analysis").label("has_calorimetry"),
    func.bool_or(resource_analysis_map.c.type == "xrd analysis").label("has_xrd"),
    func.bool_or(resource_analysis_map.c.type == "ftnir analysis").label("has_ftnir"),
    func.bool_or(resource_analysis_map.c.type == "fermentation").label("has_fermentation"),
    func.bool_or(resource_analysis_map.c.type == "gasification").label("has_gasification"),
    func.bool_or(resource_analysis_map.c.type == "pretreatment").label("has_pretreatment")
).select_from(resource_analysis_map)\
 .join(analysis_metrics, and_(
     func.lower(resource_analysis_map.c.record_id) == func.lower(analysis_metrics.c.record_id),
     resource_analysis_map.c.type == analysis_metrics.c.record_type
 ), isouter=True)\
 .group_by(resource_analysis_map.c.resource_id).subquery()

# Tag thresholds (10th and 90th percentiles) across all biomass data
thresholds = select(
 func.percentile_cont(0.1).within_group(resource_metrics.c.moisture_percent).label("moisture_low"),
 func.percentile_cont(0.9).within_group(resource_metrics.c.moisture_percent).label("moisture_high"),
 func.percentile_cont(0.1).within_group(resource_metrics.c.ash_percent).label("ash_low"),
 func.percentile_cont(0.9).within_group(resource_metrics.c.ash_percent).label("ash_high"),
 func.percentile_cont(0.1).within_group(resource_metrics.c.lignin_percent).label("lignin_low"),
 func.percentile_cont(0.9).within_group(resource_metrics.c.lignin_percent).label("lignin_high"),
 func.percentile_cont(0.1).within_group(resource_metrics.c.sugar_content_percent).label("sugar_low"),
 func.percentile_cont(0.9).within_group(resource_metrics.c.sugar_content_percent).label("sugar_high")
).subquery()

# Resource tags generation
resource_tags = select(
     resource_metrics.c.resource_id,
     func.array_remove(
         pg_array([
             case((resource_metrics.c.moisture_percent <= thresholds.c.moisture_low, "low moisture"), else_=None),
             case((resource_metrics.c.moisture_percent >= thresholds.c.moisture_high, "high moisture"), else_=None),
             case((resource_metrics.c.ash_percent <= thresholds.c.ash_low, "low ash"), else_=None),
             case((resource_metrics.c.ash_percent >= thresholds.c.ash_high, "high ash"), else_=None),
             case((resource_metrics.c.lignin_percent <= thresholds.c.lignin_low, "low lignin"), else_=None),
             case((resource_metrics.c.lignin_percent >= thresholds.c.lignin_high, "high lignin"), else_=None),
             case((resource_metrics.c.sugar_content_percent <= thresholds.c.sugar_low, "low sugar"), else_=None),
             case((resource_metrics.c.sugar_content_percent >= thresholds.c.sugar_high, "high sugar"), else_=None)
         ]),
         None
     ).label("tags")
 ).select_from(resource_metrics).join(thresholds, true()).subquery()

# Aggregated volume from Billion Ton
agg_vol = select(
     BillionTon2023Record.resource_id,
     func.sum(BillionTon2023Record.production).label("total_annual_volume"),
     func.count(func.distinct(BillionTon2023Record.geoid)).label("county_count"),
     func.max(Unit.name).label("volume_unit")
 ).join(Unit, BillionTon2023Record.production_unit_id == Unit.id)\
  .group_by(BillionTon2023Record.resource_id).subquery()

# Biomass availability aggregation
from .mv_biomass_availability import mv_biomass_availability

# Transport notes subquery (latest observation per resource)
transport_notes_sq = select(
    ResourceTransportRecord.resource_id,
    func.max(ResourceTransportRecord.transport_description).label("transport_notes")
).group_by(ResourceTransportRecord.resource_id).subquery()

# Storage notes subquery (latest observation per resource)
storage_notes_sq = select(
    ResourceStorageRecord.resource_id,
    func.max(ResourceStorageRecord.storage_description).label("storage_notes")
).group_by(ResourceStorageRecord.resource_id).subquery()

# Fallback primary product subquery for resources whose direct FK has not yet been populated.
resource_primary_product_sq = select(
    ResourceUsdaCommodityMap.resource_id,
    func.max(PrimaryAgProduct.name).label("primary_product_fallback")
).select_from(ResourceUsdaCommodityMap)\
 .join(PrimaryAgProduct, ResourceUsdaCommodityMap.primary_ag_product_id == PrimaryAgProduct.id)\
 .where(ResourceUsdaCommodityMap.resource_id.is_not(None))\
 .group_by(ResourceUsdaCommodityMap.resource_id).subquery()

mv_biomass_search = select(
     Resource.id,
     Resource.name,
     Resource.resource_code,
     Resource.description,
     ResourceClass.name.label("resource_class"),
     ResourceSubclass.name.label("resource_subclass"),
     func.coalesce(PrimaryAgProduct.name, resource_primary_product_sq.c.primary_product_fallback).label("primary_product"),
     ResourceMorphology.morphology_uri.label("image_url"),
     Resource.uri.label("literature_uri"),
     agg_vol.c.total_annual_volume,
     agg_vol.c.county_count,
     agg_vol.c.volume_unit,
     resource_metrics.c.moisture_percent,
     resource_metrics.c.sugar_content_percent,
     resource_metrics.c.ash_percent,
     resource_metrics.c.lignin_percent,
     resource_metrics.c.carbon_percent,
     resource_metrics.c.hydrogen_percent,
     resource_metrics.c.cn_ratio,
    cast(transport_notes_sq.c.transport_notes, Text).label("transport_description"),
    cast(storage_notes_sq.c.storage_notes, Text).label("storage_description"),
     transport_notes_sq.c.transport_notes,
     storage_notes_sq.c.storage_notes,
     func.coalesce(resource_tags.c.tags, cast(pg_array([]), ARRAY(String))).label("tags"),
     mv_biomass_availability.c.from_month.label("season_from_month"),
     mv_biomass_availability.c.to_month.label("season_to_month"),
     mv_biomass_availability.c.year_round,
     # Boolean flags
     func.coalesce(resource_metrics.c.has_proximate, False).label("has_proximate"),
     func.coalesce(resource_metrics.c.has_compositional, False).label("has_compositional"),
     func.coalesce(resource_metrics.c.has_ultimate, False).label("has_ultimate"),
     func.coalesce(resource_metrics.c.has_xrf, False).label("has_xrf"),
     func.coalesce(resource_metrics.c.has_icp, False).label("has_icp"),
     func.coalesce(resource_metrics.c.has_calorimetry, False).label("has_calorimetry"),
     func.coalesce(resource_metrics.c.has_xrd, False).label("has_xrd"),
     func.coalesce(resource_metrics.c.has_ftnir, False).label("has_ftnir"),
     func.coalesce(resource_metrics.c.has_fermentation, False).label("has_fermentation"),
     func.coalesce(resource_metrics.c.has_gasification, False).label("has_gasification"),
     func.coalesce(resource_metrics.c.has_pretreatment, False).label("has_pretreatment"),
     case((resource_metrics.c.moisture_percent != None, True), else_=False).label("has_moisture_data"),
     case((resource_metrics.c.sugar_content_percent > 0, True), else_=False).label("has_sugar_data"),
     case((ResourceMorphology.morphology_uri != None, True), else_=False).label("has_image"),
     case((agg_vol.c.total_annual_volume != None, True), else_=False).label("has_volume_data"),
     Resource.created_at,
     Resource.updated_at,
     func.to_tsvector(text("'english'"),
         func.coalesce(Resource.name, '') + ' ' +
         func.coalesce(Resource.description, '') + ' ' +
         func.coalesce(ResourceClass.name, '') + ' ' +
         func.coalesce(ResourceSubclass.name, '') + ' ' +
         func.coalesce(PrimaryAgProduct.name, resource_primary_product_sq.c.primary_product_fallback, '')
     ).label("search_vector")
 ).select_from(Resource)\
  .outerjoin(ResourceClass, Resource.resource_class_id == ResourceClass.id)\
  .outerjoin(ResourceSubclass, Resource.resource_subclass_id == ResourceSubclass.id)\
  .outerjoin(PrimaryAgProduct, Resource.primary_ag_product_id == PrimaryAgProduct.id)\
  .outerjoin(ResourceMorphology, ResourceMorphology.resource_id == Resource.id)\
  .outerjoin(agg_vol, agg_vol.c.resource_id == Resource.id)\
  .outerjoin(resource_metrics, resource_metrics.c.resource_id == Resource.id)\
  .outerjoin(resource_tags, resource_tags.c.resource_id == Resource.id)\
  .outerjoin(mv_biomass_availability, mv_biomass_availability.c.resource_id == Resource.id)\
  .outerjoin(transport_notes_sq, transport_notes_sq.c.resource_id == Resource.id)\
  .outerjoin(storage_notes_sq, storage_notes_sq.c.resource_id == Resource.id)\
    .outerjoin(resource_primary_product_sq, resource_primary_product_sq.c.resource_id == Resource.id)\
  .where(func.lower(Resource.name) != 'sargassum')
