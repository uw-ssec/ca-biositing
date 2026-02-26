"""
Materialized view definitions using SQLAlchemy Core select() expressions.

This module defines all 7 materialized views for the ca_biositing schema:
- landiq_record_view: LandIQ spatial records with crop mapping
- landiq_tileset_view: LandIQ geospatial tile aggregation
- analysis_data_view: Aim1 analytical records union with spatial joins
- usda_census_view: USDA Census records with commodity and place joins
- usda_survey_view: USDA Survey records with commodity and place joins
- billion_ton_tileset_view: Billion Ton 2023 records with spatial joins
- analysis_average_view: Aggregated analysis statistics (raw SQL)

Views are created via Alembic migrations and can be refreshed via refresh_all_views().
"""

from sqlalchemy import cast, func, literal, literal_column, select, text, String, Float
from sqlalchemy.orm import aliased

# Import all models needed for view definitions
from .models import (
    # External data models
    LandiqRecord,
    Polygon,
    PrimaryAgProduct,
    UsdaCensusRecord,
    UsdaSurveyRecord,
    UsdaCommodity,
    BillionTon2023Record,
    # General analysis models
    Observation,
    Parameter,
    Unit,
    DimensionType,
    # Aim1 record models
    ProximateRecord,
    UltimateRecord,
    CompositionalRecord,
    IcpRecord,
    XrfRecord,
    CalorimetryRecord,
    XrdRecord,
    # Aim2 record models
    FermentationRecord,
    PretreatmentRecord,
    # Sample models
    PreparedSample,
    FieldSample,
    # Resource and place models
    Resource,
    Place,
)

# Schema for all materialized views
VIEW_SCHEMA = "ca_biositing"

# Raw column reference for geometry — bypasses GeoAlchemy2's ST_AsEWKB wrapping
_geom_col = literal_column("polygon.geom").label("geom")

# --- 1. landiq_record_view ---
LANDIQ_RECORD_VIEW = (
    select(
        LandiqRecord.record_id,
        _geom_col,
        Polygon.geoid,
        PrimaryAgProduct.name.label("crop_name"),
        LandiqRecord.acres,
        LandiqRecord.irrigated,
        LandiqRecord.confidence,
        LandiqRecord.dataset_id,
    )
    .join(Polygon, LandiqRecord.polygon_id == Polygon.id)
    .join(PrimaryAgProduct, LandiqRecord.main_crop == PrimaryAgProduct.id)
)

# --- 2. landiq_tileset_view ---
LANDIQ_TILESET_VIEW = (
    select(
        LandiqRecord.id,
        _geom_col,
        PrimaryAgProduct.name.label("main_crop"),
        LandiqRecord.acres,
        LandiqRecord.county,
        Polygon.geoid,
        LandiqRecord.dataset_id.label("tileset_id"),
    )
    .join(Polygon, LandiqRecord.polygon_id == Polygon.id)
    .join(PrimaryAgProduct, LandiqRecord.main_crop == PrimaryAgProduct.id)
)

# --- 3. analysis_data_view ---
ANALYSIS_DATA_VIEW = (
    select(
        Observation.id,
        Observation.record_id,
        Observation.record_type,
        Resource.name.label("resource"),
        literal("06000").label("geoid"),
        Parameter.name.label("parameter"),
        Observation.value,
        Unit.name.label("unit"),
        DimensionType.name.label("dimension_type"),
        Observation.dimension_value,
        DimensionUnit.name.label("dimension_unit"),
    )
    .join(Parameter, Observation.parameter_id == Parameter.id)
    .join(Unit, Observation.unit_id == Unit.id)
    .outerjoin(DimensionType, Observation.dimension_type_id == DimensionType.id)
    .outerjoin(DimensionUnit, Observation.dimension_unit_id == DimensionUnit.id)
    .outerjoin(
        ProximateRecord,
        (Observation.record_id == ProximateRecord.record_id)
        & (Observation.record_type == "proximate analysis"),
    )
    .outerjoin(
        UltimateRecord,
        (Observation.record_id == UltimateRecord.record_id)
        & (Observation.record_type == "ultimate analysis"),
    )
    .outerjoin(
        CompositionalRecord,
        (Observation.record_id == CompositionalRecord.record_id)
        & (Observation.record_type == "compositional analysis"),
    )
    .outerjoin(
        IcpRecord,
        (Observation.record_id == IcpRecord.record_id)
        & (
            (Observation.record_type == "icp analysis")
            | (Observation.record_type == "icp-oes")
            | (Observation.record_type == "icp-ms")
        ),
    )
    .outerjoin(
        XrfRecord,
        (Observation.record_id == XrfRecord.record_id)
        & (Observation.record_type == "xrf analysis"),
    )
    .outerjoin(
        CalorimetryRecord,
        (Observation.record_id == CalorimetryRecord.record_id)
        & (Observation.record_type == "calorimetry analysis"),
    )
    .outerjoin(
        XrdRecord,
        (Observation.record_id == XrdRecord.record_id)
        & (Observation.record_type == "xrd analysis"),
    )
    .outerjoin(
        FermentationRecord,
        (Observation.record_id == FermentationRecord.record_id)
        & (Observation.record_type == "fermentation"),
    )
    .outerjoin(
        PretreatmentRecord,
        (Observation.record_id == PretreatmentRecord.record_id)
        & (Observation.record_type == "pretreatment"),
    )
    .outerjoin(
        Resource,
        Resource.id
        == func.coalesce(
            ProximateRecord.resource_id,
            UltimateRecord.resource_id,
            CompositionalRecord.resource_id,
            IcpRecord.resource_id,
            XrfRecord.resource_id,
            CalorimetryRecord.resource_id,
            XrdRecord.resource_id,
            FermentationRecord.resource_id,
            PretreatmentRecord.resource_id,
        ),
    )
)

# --- 4. usda_census_view ---
# Create aliased Unit for dimension_unit
DimensionUnit = aliased(Unit, name="du")

USDA_CENSUS_VIEW = (
    select(
        Observation.id,
        UsdaCommodity.name.label("usda_crop"),
        Place.geoid,
        Parameter.name.label("parameter"),
        Observation.value,
        Unit.name.label("unit"),
        DimensionType.name.label("dimension"),
        Observation.dimension_value,
        DimensionUnit.name.label("dimension_unit"),
    )
    .join(
        UsdaCensusRecord,
        (Observation.record_id == cast(UsdaCensusRecord.id, String))
        & (Observation.record_type == "usda_census_record"),
    )
    .join(UsdaCommodity, UsdaCensusRecord.commodity_code == UsdaCommodity.id)
    .join(Place, UsdaCensusRecord.geoid == Place.geoid)
    .join(Parameter, Observation.parameter_id == Parameter.id)
    .join(Unit, Observation.unit_id == Unit.id)
    .outerjoin(DimensionType, Observation.dimension_type_id == DimensionType.id)
    .outerjoin(DimensionUnit, Observation.dimension_unit_id == DimensionUnit.id)
)

# --- 5. usda_survey_view ---
# Mirrors usda_census_view with UsdaSurveyRecord
USDA_SURVEY_VIEW = (
    select(
        Observation.id,
        UsdaCommodity.name.label("usda_crop"),
        Place.geoid,
        Parameter.name.label("parameter"),
        Observation.value,
        Unit.name.label("unit"),
        DimensionType.name.label("dimension"),
        Observation.dimension_value,
        DimensionUnit.name.label("dimension_unit"),
    )
    .join(
        UsdaSurveyRecord,
        (Observation.record_id == cast(UsdaSurveyRecord.id, String))
        & (Observation.record_type == "usda_survey_record"),
    )
    .join(UsdaCommodity, UsdaSurveyRecord.commodity_code == UsdaCommodity.id)
    .join(Place, UsdaSurveyRecord.geoid == Place.geoid)
    .join(Parameter, Observation.parameter_id == Parameter.id)
    .join(Unit, Observation.unit_id == Unit.id)
    .outerjoin(DimensionType, Observation.dimension_type_id == DimensionType.id)
    .outerjoin(DimensionUnit, Observation.dimension_unit_id == DimensionUnit.id)
)

# --- 6. billion_ton_tileset_view ---
BILLION_TON_TILESET_VIEW = (
    select(
        BillionTon2023Record.id,
        Resource.name.label("resource"),
        Place.county_name.label("county"),
        literal("production").label("parameter"),
        cast(BillionTon2023Record.production, Float).label("value"),
        Unit.name.label("unit"),
        BillionTon2023Record.etl_run_id.label("tileset_id"),
    )
    .join(Resource, BillionTon2023Record.resource_id == Resource.id)
    .join(Place, BillionTon2023Record.geoid == Place.geoid)
    .join(Unit, BillionTon2023Record.production_unit_id == Unit.id)
)

# --- 7. analysis_average_view --- (SPECIAL CASE: depends on analysis_data_view)
# Cannot use Core select() against models because it aggregates another mat view.
# Use raw SQL string instead:
ANALYSIS_AVERAGE_VIEW_SQL = """
    SELECT resource, geoid, parameter,
           AVG(value) as average_value,
           STDDEV(value) as standard_deviation,
           unit, COUNT(*) as observation_count
    FROM ca_biositing.analysis_data_view
    GROUP BY resource, geoid, parameter, unit
"""

# Ordered list for creation (respects inter-view dependencies)
VIEW_DEFINITIONS = [
    ("landiq_record_view", LANDIQ_RECORD_VIEW),
    ("landiq_tileset_view", LANDIQ_TILESET_VIEW),
    ("analysis_data_view", ANALYSIS_DATA_VIEW),
    ("usda_census_view", USDA_CENSUS_VIEW),
    ("usda_survey_view", USDA_SURVEY_VIEW),
    ("billion_ton_tileset_view", BILLION_TON_TILESET_VIEW),
    # analysis_average_view is last (depends on analysis_data_view)
]

# Views requiring GIST spatial indexes
SPATIAL_VIEW_INDEXES = [
    ("idx_landiq_record_view_geom", "landiq_record_view", "geom"),
    ("idx_landiq_tileset_view_geom", "landiq_tileset_view", "geom"),
]


def refresh_all_views(engine):
    """Refresh all materialized views in dependency order.

    Args:
        engine: SQLAlchemy engine instance connected to the database.

    Example:
        from ca_biositing.datamodels.database import get_engine
        from ca_biositing.datamodels.views import refresh_all_views

        engine = get_engine()
        refresh_all_views(engine)
    """
    with engine.connect() as conn:
        for view_name, _ in VIEW_DEFINITIONS:
            conn.execute(text(f"REFRESH MATERIALIZED VIEW {VIEW_SCHEMA}.{view_name}"))
        conn.execute(text(f"REFRESH MATERIALIZED VIEW {VIEW_SCHEMA}.analysis_average_view"))
        conn.commit()
