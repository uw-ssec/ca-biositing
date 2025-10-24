from __future__ import annotations

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Index

# ----------------------------------------------------------------------
# External / third‑party data tables
# ----------------------------------------------------------------------


class ExternalDairyOne(SQLModel, table=True):
    """External data from the Dairy‑One dataset."""
    __tablename__ = "external_dairy_one"

    dairy_one_id: Optional[int] = Field(default=None, primary_key=True)
    data_source_id: Optional[int] = Field(default=None,
                                          description="Reference to data_sources.source_id")
                                          # foreign_key="data_sources.source_id")
    biomass_id: Optional[int] = Field(default=None,
                                      description="Reference to biomass.biomass_id")
                                      # foreign_key="biomass.biomass_id")
    analysis_type_id: Optional[int] = Field(default=None,
                                            description="Reference to analysis_types.analysis_type_id")
                                            # foreign_key="analysis_types.analysis_type_id")
    parameter_id: Optional[int] = Field(default=None,
                                        description="Reference to parameters.parameter_id")
                                        # foreign_key="parameters.parameter_id")
    parameter_method_id: Optional[int] = Field(default=None,
                                               description="Reference to parameter_methods.param_method_id")
                                               # foreign_key="parameter_methods.param_method_id")
    samples_count: Optional[int] = Field(default=None)
    mean_value: Optional[Decimal] = Field(default=None)
    std_dev: Optional[Decimal] = Field(default=None)
    min_value: Optional[Decimal] = Field(default=None)
    max_value: Optional[Decimal] = Field(default=None)
    unit_id: Optional[int] = Field(default=None,
                                   description="Reference to units.unit_id")
                                   # foreign_key="units.unit_id")
    methodology_reference_id: Optional[int] = Field(default=None,
                                                   description="Reference to methods.method_id")
                                                   # foreign_key="methods.method_id")
    accumulated_years_from: Optional[date] = Field(default=None)
    accumulated_years_to: Optional[date] = Field(default=None)
    import_date: Optional[date] = Field(default=None)

    __table_args__ = (
        Index("idx_external_dairy_one_biomass_id", "biomass_id"),
        Index("idx_external_dairy_one_parameter_id", "parameter_id"),
    )


class ExternalINLBiofeedstockLibrary(SQLModel, table=True):
    """INL Bio‑Feedstock Library external data."""
    __tablename__ = "external_inl_biofeedstock_library"

    bfl_id: Optional[int] = Field(default=None, primary_key=True)
    data_source_id: Optional[int] = Field(default=None,
                                          description="Reference to data_sources.source_id")
                                          # foreign_key="data_sources.source_id")
    sample_id: Optional[int] = Field(default=None,
                                     description="Reference to field_samples.sample_id")
                                     # foreign_key="field_samples.sample_id")
    biomass_id: Optional[int] = Field(default=None,
                                      description="Reference to biomass.biomass_id")
                                      # foreign_key="biomass.biomass_id")
    analysis_type_id: Optional[int] = Field(default=None,
                                            description="Reference to analysis_types.analysis_type_id")
                                            # foreign_key="analysis_types.analysis_type_id")
    state_id: Optional[int] = Field(default=None,
                                    description="Reference to states.state_id")
                                    # foreign_key="states.state_id")
    affiliations_id: Optional[int] = Field(default=None,
                                          description="Reference to affiliations.affiliation_id")
                                          # foreign_key="affiliations.affiliation_id")
    harvest_method_id: Optional[int] = Field(default=None,
                                             description="Reference to harvest_methods.harvest_method_id")
                                             # foreign_key="harvest_methods.harvest_method_id")
    collection_method_id: Optional[int] = Field(default=None,
                                                description="Reference to collection_methods.collection_method_id")
                                                # foreign_key="collection_methods.collection_method_id")
    parameter_id: Optional[int] = Field(default=None,
                                        description="Reference to parameters.parameter_id")
                                        # foreign_key="parameters.parameter_id")
    parameter_method_id: Optional[int] = Field(default=None,
                                               description="Reference to parameter_methods.param_method_id")
                                               # foreign_key="parameter_methods.param_method_id")
    mean_value: Optional[Decimal] = Field(default=None)
    std_dev: Optional[Decimal] = Field(default=None)
    min_value: Optional[Decimal] = Field(default=None)
    max_value: Optional[Decimal] = Field(default=None)
    sample_count: Optional[int] = Field(default=None)
    unit_id: Optional[int] = Field(default=None,
                                   description="Reference to units.unit_id")
                                   # foreign_key="units.unit_id")
    methodology_reference_id: Optional[int] = Field(default=None,
                                                   description="Reference to methods.method_id")
                                                   # foreign_key="methods.method_id")
    accumulated_years_from: Optional[date] = Field(default=None)
    accumulated_years_to: Optional[date] = Field(default=None)
    import_date: Optional[date] = Field(default=None)

    __table_args__ = (
        Index("idx_external_inl_biofeedstock_library_biomass_id", "biomass_id"),
    )


class ExternalPhyllis2(SQLModel, table=True):
    """External literature data (Phyllis2)."""
    __tablename__ = "external_phyllis2"

    phyllis_id: Optional[int] = Field(default=None, primary_key=True)
    data_source_id: Optional[int] = Field(default=None,
                                          description="Reference to data_sources.source_id")
                                          # foreign_key="data_sources.source_id")
    biomass_id: Optional[int] = Field(default=None,
                                      description="Reference to biomass.biomass_id")
                                      # foreign_key="biomass.biomass_id")
    analysis_type_id: Optional[int] = Field(default=None,
                                            description="Reference to analysis_types.analysis_type_id")
                                            # foreign_key="analysis_types.analysis_type_id")
    parameter_id: Optional[int] = Field(default=None,
                                        description="Reference to parameters.parameter_id")
                                        # foreign_key="parameters.parameter_id")
    parameter_method_id: Optional[int] = Field(default=None,
                                               description="Reference to parameter_methods.param_method_id")
                                               # foreign_key="parameter_methods.param_method_id")
    mean_value: Optional[Decimal] = Field(default=None)
    std_dev: Optional[Decimal] = Field(default=None)
    max_value: Optional[Decimal] = Field(default=None)
    sample_count: Optional[int] = Field(default=None)
    unit_id: Optional[int] = Field(default=None,
                                   description="Reference to units.unit_id")
                                   # foreign_key="units.unit_id")
    methodology_reference_id: Optional[int] = Field(default=None,
                                                   description="Reference to methods.method_id")
                                                   # foreign_key="methods.method_id")
    import_date: Optional[date] = Field(default=None)

    __table_args__ = (
        Index("idx_external_phyllis2_biomass_id", "biomass_id"),
        Index("idx_external_phyllis2_analysis_type_id", "analysis_type_id"),
    )


class ExternalEBMUD(SQLModel, table=True):
    """External EBMUD dataset."""
    __tablename__ = "external_ebmud"

    ebmud_id: Optional[int] = Field(default=None, primary_key=True)
    data_source_id: Optional[int] = Field(default=None,
                                          description="Reference to data_sources.source_id")
                                          # foreign_key="data_sources.source_id")
    biomass_id: Optional[int] = Field(default=None,
                                      description="Reference to biomass.biomass_id")
                                      # foreign_key="biomass.biomass_id")
    analysis_type_id: Optional[int] = Field(default=None,
                                            description="Reference to analysis_types.analysis_type_id")
                                            # foreign_key="analysis_types.analysis_type_id")
    parameter_id: Optional[int] = Field(default=None,
                                        description="Reference to parameters.parameter_id")
                                        # foreign_key="parameters.parameter_id")
    parameter_method_id: Optional[int] = Field(default=None,
                                               description="Reference to parameter_methods.param_method_id")
                                               # foreign_key="parameter_methods.param_method_id")
    mean_value: Optional[Decimal] = Field(default=None)
    std_dev: Optional[Decimal] = Field(default=None)
    min_value: Optional[Decimal] = Field(default=None)
    max_value: Optional[Decimal] = Field(default=None)
    sample_count: Optional[int] = Field(default=None)
    unit_id: Optional[int] = Field(default=None,
                                   description="Reference to units.unit_id")
                                   # foreign_key="units.unit_id")
    import_date: Optional[date] = Field(default=None)


class VectorizedRasterPolygon(SQLModel, table=True):
    """Polygon derived from a raster (PostGIS geometry)."""
    __tablename__ = "vectorized_raster_polygons"

    vectorized_ID: Optional[int] = Field(default=None, primary_key=True)
    geometry: Optional[str] = Field(default=None,
                                    description="Polygon geometry (PostGIS), use appropriate SRID")
    raster_id: Optional[int] = Field(default=None,
                                     description="Optional foreign key to raster_metadata.id")
                                     # foreign_key="raster_metadata.id")
    class_: Optional[str] = Field(default=None,
                                  description="Classification label or category (e.g., land use type)",
                                  alias="class")
    value: Optional[float] = Field(default=None,
                                    description="Raw pixel value this polygon was derived from")
    mean_value: Optional[float] = Field(default=None,
                                         description="Mean raster value within the polygon")
    std_dev: Optional[float] = Field(default=None,
                                      description="Standard deviation of raster values in the polygon")
    area_m2: Optional[float] = Field(default=None,
                                     description="Area of the polygon in square meters")
    date_acquired: Optional[date] = Field(default=None,
                                          description="Date the source raster was collected")
    source: Optional[str] = Field(default=None,
                                  description="Source of the raster (e.g., Sentinel‑2)")
    notes: Optional[str] = Field(default=None,
                                 description="Additional optional metadata or remarks")


class RasterMetadata(SQLModel, table=True):
    """Metadata for raster layers."""
    __tablename__ = "raster_metadata"

    id: Optional[int] = Field(default=None, primary_key=True)
    source: Optional[str] = Field(default=None,
                                  description="Data source name or provider")
    resolution: Optional[float] = Field(default=None,
                                        description="Raster resolution in meters")
    srid: Optional[int] = Field(default=None,
                                 description="Spatial reference ID used in raster")
    acquisition_date: Optional[date] = Field(default=None,
                                             description="Date of raster acquisition")
    notes: Optional[str] = Field(default=None,
                                 description="Any additional metadata")


class ExternalATIP(SQLModel, table=True):
    """ATIP external geospatial data."""
    __tablename__ = "external_atip"

    atip_ID: Optional[int] = Field(default=None, primary_key=True)
    biomass_id: Optional[int] = Field(default=None,
                                      description="Reference to biomass.biomass_id")
                                      # foreign_key="biomass.biomass_id")
    location_id: Optional[int] = Field(default=None,
                                       description="Reference to geographic_locations.location_id")
                                       # foreign_key="geographic_locations.location_id")
    parameter_id: Optional[int] = Field(default=None,
                                        description="Reference to parameters.parameter_id")
                                        # foreign_key="parameters.parameter_id")
    value: Optional[Decimal] = Field(default=None)
    unit_id: Optional[int] = Field(default=None,
                                   description="Reference to units.unit_id")
                                   # foreign_key="units.unit_id")
    geometry_id: Optional[int] = Field(default=None)
    geometry: Optional[str] = Field(default=None,
                                    description="Geometry (PostGIS geom type)")
    import_date: Optional[date] = Field(default=None)


class ExternalLandIQ(SQLModel, table=True):
    """Land‑IQ external geospatial data."""
    __tablename__ = "external_land_id"

    land_id: Optional[int] = Field(default=None, primary_key=True)  # renamed from land_id_id
    biomass_id: Optional[int] = Field(default=None,
                                      description="Reference to biomass.biomass_id")
                                      # foreign_key="biomass.biomass_id")
    location_id: Optional[int] = Field(default=None,
                                       description="Reference to geographic_locations.location_id")
                                       # foreign_key="geographic_locations.location_id")
    parameter_id: Optional[int] = Field(default=None,
                                        description="Reference to parameters.parameter_id")
                                        # foreign_key="parameters.parameter_id")
    value: Optional[Decimal] = Field(default=None)
    unit_id: Optional[int] = Field(default=None,
                                   description="Reference to units.unit_id")
                                   # foreign_key="units.unit_id")
    geometry_id: Optional[int] = Field(default=None)
    geometry: Optional[str] = Field(default=None,
                                    description="Geometry (PostGIS geom type)")
    import_date: Optional[date] = Field(default=None)


class ExternalUSDA(SQLModel, table=True):
    """USDA external geospatial data."""
    __tablename__ = "external_usda"

    usda_id: Optional[int] = Field(default=None, primary_key=True)
    biomass_id: Optional[int] = Field(default=None,
                                      description="Reference to biomass.biomass_id")
                                      # foreign_key="biomass.biomass_id")
    location_id: Optional[int] = Field(default=None,
                                       description="Reference to geographic_locations.location_id")
                                       # foreign_key="geographic_locations.location_id")
    parameter_id: Optional[int] = Field(default=None,
                                        description="Reference to parameters.parameter_id")
                                        # foreign_key="parameters.parameter_id")
    value: Optional[Decimal] = Field(default=None)
    unit_id: Optional[int] = Field(default=None,
                                   description="Reference to units.unit_id")
                                   # foreign_key="units.unit_id")
    geometry_id: Optional[int] = Field(default=None)
    geometry: Optional[str] = Field(default=None,
                                    description="Geometry (PostGIS geom type)")
    import_date: Optional[date] = Field(default=None)
