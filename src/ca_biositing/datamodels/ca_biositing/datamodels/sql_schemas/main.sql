--
-- pgschema database dump (Automated Topological Sort)
--

-- Extensions & Types
\i types/geometry_dump.sql
\i types/valid_detail.sql

-- Schemas
\i schemas.sql

-- Tables (Dependency Sorted)
\i tables/infrastructure_district_energy_systems.sql
\i tables/etl_run.sql
\i tables/source_type.sql
\i tables/data_source_type.sql
\i tables/location_resolution.sql
\i tables/data_source.sql
\i tables/place.sql
\i tables/location_address.sql
\i tables/usda_market_report.sql
\i tables/dataset.sql
\i tables/unit.sql
\i tables/usda_commodity.sql
\i tables/usda_market_record.sql
\i tables/infrastructure_ethanol_biorefineries.sql
\i tables/file_object_metadata.sql
\i tables/contact.sql
\i tables/experiment.sql
\i tables/primary_ag_product.sql
\i tables/resource_class.sql
\i tables/resource_subclass.sql
\i tables/resource.sql
\i tables/method_abbrev.sql
\i tables/method_standard.sql
\i tables/method_category.sql
\i tables/method.sql
\i tables/preparation_method_abbreviation.sql
\i tables/preparation_method.sql
\i tables/harvest_method.sql
\i tables/collection_method.sql
\i tables/field_storage_method.sql
\i tables/provider.sql
\i tables/field_sample.sql
\i tables/prepared_sample.sql
\i tables/fermentation_record.sql
\i tables/processing_method.sql
\i tables/billion_ton2023_record.sql
\i tables/gasification_record.sql
\i tables/xrf_record.sql
\i tables/soil_type.sql
\i tables/location_soil_type.sql
\i tables/landiq_resource_mapping.sql
\i tables/infrastructure_combustion_plants.sql
\i tables/infrastructure_wastewater_treatment_plants.sql
\i tables/spatial_ref_sys.sql
\i tables/infrastructure_biosolids_facilities.sql
\i tables/aim1_record_base.sql
\i tables/physical_characteristic.sql
\i tables/icp_record.sql
\i tables/parameter.sql
\i tables/parameter_category.sql
\i tables/parameter_category_parameter.sql
\i tables/usda_census_record.sql
\i tables/lookup_base.sql
\i tables/resource_availability.sql
\i tables/strain.sql
\i tables/proximate_record.sql
\i tables/infrastructure_msw_to_energy_anaerobic_digesters.sql
\i tables/xrd_record.sql
\i tables/ftnir_record.sql
\i tables/infrastructure_saf_and_renewable_diesel_plants.sql
\i tables/ultimate_record.sql
\i tables/equipment.sql
\i tables/experiment_equipment.sql
\i tables/infrastructure_cafo_manure_locations.sql
\i tables/usda_domain.sql
\i tables/infrastructure_livestock_anaerobic_digesters.sql
\i tables/lineage_group.sql
\i tables/ag_treatment.sql
\i tables/field_sample_condition.sql
\i tables/dimension_type.sql
\i tables/observation.sql
\i tables/usda_survey_program.sql
\i tables/usda_survey_record.sql
\i tables/resource_morphology.sql
\i tables/aim2_record_base.sql
\i tables/usda_statistic_category.sql
\i tables/calorimetry_record.sql
\i tables/infrastructure_landfills.sql
\i tables/compositional_record.sql
\i tables/rgb_record.sql
\i tables/analysis_type.sql
\i tables/experiment_analysis.sql
\i tables/infrastructure_biodiesel_plants.sql
\i tables/entity_lineage.sql
\i tables/polygon.sql
\i tables/landiq_record.sql
\i tables/experiment_prepared_sample.sql
\i tables/infrastructure_food_processing_facilities.sql
\i tables/autoclave_record.sql
\i tables/alembic_version.sql
\i tables/resource_usda_commodity_map.sql
\i tables/pretreatment_record.sql
\i tables/usda_term_map.sql
\i tables/base_entity.sql
\i tables/experiment_method.sql
\i tables/parameter_unit.sql
\i tables/facility_record.sql

-- Materialized Views (Analytical Layer)
\i ca_biositing/views/landiq_record_view.sql
\i ca_biositing/views/analysis_data_view.sql
\i ca_biositing/views/landiq_tileset_view.sql
\i ca_biositing/views/usda_census_view.sql
\i ca_biositing/views/analysis_average_view.sql
\i ca_biositing/views/billion_ton_tileset_view.sql
\i ca_biositing/views/usda_survey_view.sql

-- Views
\i views/geography_columns.sql
\i views/geometry_columns.sql

-- Privileges
\i privileges/table.sql
\i privileges/view.sql
