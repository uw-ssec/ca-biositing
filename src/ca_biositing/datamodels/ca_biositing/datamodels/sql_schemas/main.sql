--
-- pgschema database dump
--

-- Dumped from database version PostgreSQL 15.4
-- Dumped by pgschema version 1.6.2


--
-- Name: geometry_dump; Type: TYPE; Schema: -; Owner: -
--

CREATE TYPE geometry_dump AS (path integer[], geom geometry);

--
-- Name: valid_detail; Type: TYPE; Schema: -; Owner: -
--

CREATE TYPE valid_detail AS (valid boolean, reason character varying, location geometry);

--
-- Name: ag_treatment; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS ag_treatment (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT ag_treatment_pkey PRIMARY KEY (id)
);

--
-- Name: alembic_version; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS alembic_version (
    version_num varchar(32),
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

--
-- Name: analysis_type; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS analysis_type (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT analysis_type_pkey PRIMARY KEY (id)
);

--
-- Name: collection_method; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS collection_method (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT collection_method_pkey PRIMARY KEY (id)
);

--
-- Name: dimension_type; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS dimension_type (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT dimension_type_pkey PRIMARY KEY (id)
);

--
-- Name: entity_lineage; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS entity_lineage (
    id SERIAL,
    lineage_group_id integer,
    source_table varchar,
    source_row_id varchar,
    note varchar,
    CONSTRAINT entity_lineage_pkey PRIMARY KEY (id)
);

--
-- Name: etl_run; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS etl_run (
    id SERIAL,
    run_id varchar,
    started_at timestamp,
    completed_at timestamp,
    pipeline_name varchar,
    status varchar,
    records_ingested integer,
    note varchar,
    CONSTRAINT etl_run_pkey PRIMARY KEY (id)
);

--
-- Name: contact; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS contact (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    name varchar,
    first_name varchar,
    last_name varchar,
    email varchar,
    affiliation varchar,
    CONSTRAINT contact_pkey PRIMARY KEY (id),
    CONSTRAINT contact_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id)
);

--
-- Name: field_storage_method; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS field_storage_method (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT field_storage_method_pkey PRIMARY KEY (id)
);

--
-- Name: harvest_method; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS harvest_method (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT harvest_method_pkey PRIMARY KEY (id)
);

--
-- Name: infrastructure_biodiesel_plants; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_biodiesel_plants (
    biodiesel_plant_id SERIAL,
    company varchar,
    bbi_index integer,
    city varchar,
    state varchar,
    capacity_mmg_per_y integer,
    feedstock varchar,
    status varchar,
    address varchar,
    coordinates varchar,
    latitude numeric,
    longitude numeric,
    source varchar,
    CONSTRAINT infrastructure_biodiesel_plants_pkey PRIMARY KEY (biodiesel_plant_id)
);

--
-- Name: infrastructure_biosolids_facilities; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_biosolids_facilities (
    biosolid_facility_id SERIAL,
    report_submitted_date date,
    latitude numeric,
    longitude numeric,
    facility varchar,
    authority varchar,
    plant_type varchar,
    aqmd varchar,
    facility_address varchar,
    facility_city varchar,
    state varchar,
    facility_zip varchar,
    facility_county varchar,
    mailing_street_1 varchar,
    mailing_city varchar,
    mailing_state varchar,
    mailing_zip varchar,
    biosolids_number varchar,
    biosolids_contact varchar,
    biosolids_contact_phone varchar,
    biosolids_contact_email varchar,
    adwf numeric,
    potw_biosolids_generated integer,
    twtds_biosolids_treated integer,
    class_b_land_app integer,
    class_b_applier varchar,
    class_a_compost integer,
    class_a_heat_dried integer,
    class_a_other integer,
    class_a_other_applier varchar,
    twtds_transfer_to_second_preparer integer,
    twtds_second_preparer_name varchar,
    adc_or_final_c integer,
    landfill integer,
    landfill_name varchar,
    surface_disposal integer,
    deepwell_injection varchar,
    stored integer,
    longterm_treatment integer,
    other integer,
    name_of_other varchar,
    incineration integer,
    CONSTRAINT infrastructure_biosolids_facilities_pkey PRIMARY KEY (biosolid_facility_id)
);

--
-- Name: infrastructure_cafo_manure_locations; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_cafo_manure_locations (
    cafo_manure_id SERIAL,
    latitude numeric,
    longitude numeric,
    owner_name varchar,
    facility_name varchar,
    address varchar,
    town varchar,
    state varchar,
    zip varchar,
    animal varchar,
    animal_feed_operation_type varchar,
    animal_units integer,
    animal_count integer,
    manure_total_solids numeric,
    source varchar,
    date_accessed date,
    CONSTRAINT infrastructure_cafo_manure_locations_pkey PRIMARY KEY (cafo_manure_id)
);

--
-- Name: infrastructure_combustion_plants; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_combustion_plants (
    combustion_fid SERIAL,
    objectid integer,
    status varchar,
    city varchar,
    name varchar,
    county varchar,
    equivalent_generation numeric,
    np_mw numeric,
    cf numeric,
    yearload integer,
    fuel varchar,
    notes varchar,
    type varchar,
    wkt_geom varchar,
    geom varchar,
    latitude numeric,
    longitude numeric,
    CONSTRAINT infrastructure_combustion_plants_pkey PRIMARY KEY (combustion_fid)
);

--
-- Name: infrastructure_district_energy_systems; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_district_energy_systems (
    des_fid SERIAL,
    cbg_id integer,
    name varchar,
    system varchar,
    object_id integer,
    city varchar,
    state varchar,
    primary_fuel varchar,
    secondary_fuel varchar,
    usetype varchar,
    cap_st numeric,
    cap_hw numeric,
    cap_cw numeric,
    chpcg_cap numeric,
    excess_c numeric,
    excess_h numeric,
    type varchar,
    wkt_geom varchar,
    geom varchar,
    latitude numeric,
    longitude numeric,
    CONSTRAINT infrastructure_district_energy_systems_pkey PRIMARY KEY (des_fid)
);

--
-- Name: infrastructure_ethanol_biorefineries; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_ethanol_biorefineries (
    ethanol_biorefinery_id SERIAL,
    name varchar,
    city varchar,
    state varchar,
    address varchar,
    type varchar,
    capacity_mgy integer,
    production_mgy integer,
    constr_exp integer,
    CONSTRAINT infrastructure_ethanol_biorefineries_pkey PRIMARY KEY (ethanol_biorefinery_id)
);

--
-- Name: infrastructure_food_processing_facilities; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_food_processing_facilities (
    processing_facility_id SERIAL,
    address varchar,
    county varchar,
    city varchar,
    company varchar,
    join_count integer,
    master_type varchar,
    state varchar,
    subtype varchar,
    target_fid integer,
    processing_type varchar,
    zip varchar,
    type varchar,
    wkt_geom varchar,
    geom varchar,
    latitude numeric,
    longitude numeric,
    CONSTRAINT infrastructure_food_processing_facilities_pkey PRIMARY KEY (processing_facility_id)
);

--
-- Name: infrastructure_landfills; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_landfills (
    project_id varchar,
    project_int_id integer,
    ghgrp_id varchar,
    landfill_id integer,
    landfill_name varchar,
    state varchar,
    physical_address varchar,
    city varchar,
    county varchar,
    zip_code varchar,
    latitude numeric,
    longitude numeric,
    ownership_type varchar,
    landfill_owner_orgs varchar,
    landfill_opened_year date,
    landfill_closure_year date,
    landfill_status varchar,
    waste_in_place integer,
    waste_in_place_year date,
    lfg_system_in_place boolean,
    lfg_collected numeric,
    lfg_flared numeric,
    project_status varchar,
    project_name varchar,
    project_start_date date,
    project_shutdown_date date,
    project_type_category varchar,
    lfg_energy_project_type varchar,
    rng_delivery_method varchar,
    actual_mw_generation numeric,
    rated_mw_capacity numeric,
    lfg_flow_to_project numeric,
    direct_emission_reductions numeric,
    avoided_emission_reductions numeric,
    CONSTRAINT infrastructure_landfills_pkey PRIMARY KEY (project_id)
);

--
-- Name: infrastructure_livestock_anaerobic_digesters; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_livestock_anaerobic_digesters (
    digester_id SERIAL,
    project_name varchar,
    project_type varchar,
    city varchar,
    state varchar,
    digester_type varchar,
    profile varchar,
    year_operational date,
    animal_type_class varchar,
    animal_types varchar,
    pop_feeding_digester varchar,
    total_pop_feeding_digester integer,
    cattle integer,
    dairy integer,
    poultry integer,
    swine integer,
    codigestion varchar,
    biogas_generation_estimate integer,
    electricity_generated integer,
    biogas_end_uses varchar,
    methane_emission_reductions integer,
    latitude numeric,
    longitude numeric,
    CONSTRAINT infrastructure_livestock_anaerobic_digesters_pkey PRIMARY KEY (digester_id)
);

--
-- Name: infrastructure_msw_to_energy_anaerobic_digesters; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_msw_to_energy_anaerobic_digesters (
    wte_id SERIAL,
    city varchar,
    county varchar,
    equivalent_generation numeric,
    feedstock varchar,
    dayload numeric,
    dayload_bdt numeric,
    facility_type varchar,
    status varchar,
    notes varchar,
    source varchar,
    type varchar,
    wkt_geom varchar,
    geom varchar,
    latitude numeric,
    longitude numeric,
    CONSTRAINT infrastructure_msw_to_energy_anaerobic_digesters_pkey PRIMARY KEY (wte_id)
);

--
-- Name: infrastructure_saf_and_renewable_diesel_plants; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_saf_and_renewable_diesel_plants (
    ibcc_index SERIAL,
    company varchar,
    city varchar,
    state varchar,
    country varchar,
    capacity varchar,
    feedstock varchar,
    products varchar,
    status varchar,
    address varchar,
    coordinates varchar,
    latitude numeric,
    longitude numeric,
    CONSTRAINT infrastructure_saf_and_renewable_diesel_plants_pkey PRIMARY KEY (ibcc_index)
);

--
-- Name: infrastructure_wastewater_treatment_plants; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS infrastructure_wastewater_treatment_plants (
    plant_id SERIAL,
    name varchar,
    state varchar,
    codigestion varchar,
    flow_design_adjusted numeric,
    flow_average numeric,
    biosolids numeric,
    excess_flow numeric,
    biogas_utilized boolean,
    flaring boolean,
    excess_mass_loading_rate numeric,
    excess_mass_loading_rate_wet numeric,
    methane_production numeric,
    energy_content numeric,
    electric_kw numeric,
    thermal_mmbtu_d numeric,
    electric_kwh numeric,
    thermal_annual_mmbtu_y numeric,
    anaerobic_digestion_facility varchar,
    county varchar,
    dayload_bdt numeric,
    dayload numeric,
    equivalent_generation numeric,
    facility_type varchar,
    feedstock varchar,
    type varchar,
    city varchar,
    latitude numeric,
    longitude numeric,
    zipcode varchar,
    CONSTRAINT infrastructure_wastewater_treatment_plants_pkey PRIMARY KEY (plant_id)
);

--
-- Name: lineage_group; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS lineage_group (
    id SERIAL,
    etl_run_id integer,
    note varchar,
    CONSTRAINT lineage_group_pkey PRIMARY KEY (id),
    CONSTRAINT lineage_group_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id)
);

--
-- Name: location_resolution; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS location_resolution (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT location_resolution_pkey PRIMARY KEY (id)
);

--
-- Name: method_abbrev; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS method_abbrev (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT method_abbrev_pkey PRIMARY KEY (id)
);

--
-- Name: method_category; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS method_category (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT method_category_pkey PRIMARY KEY (id)
);

--
-- Name: method_standard; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS method_standard (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT method_standard_pkey PRIMARY KEY (id)
);

--
-- Name: parameter_category; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS parameter_category (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT parameter_category_pkey PRIMARY KEY (id)
);

--
-- Name: place; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS place (
    geoid varchar,
    state_name varchar,
    state_fips varchar,
    county_name varchar,
    county_fips varchar,
    region_name varchar,
    agg_level_desc varchar,
    CONSTRAINT place_pkey PRIMARY KEY (geoid)
);

--
-- Name: location_address; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS location_address (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    geography_id varchar,
    address_line1 varchar,
    address_line2 varchar,
    city varchar,
    zip varchar,
    lat double precision,
    lon double precision,
    is_anonymous boolean,
    CONSTRAINT location_address_pkey PRIMARY KEY (id),
    CONSTRAINT location_address_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT location_address_geography_id_fkey FOREIGN KEY (geography_id) REFERENCES place (geoid)
);

--
-- Name: equipment; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS equipment (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    equipment_location_id integer,
    CONSTRAINT equipment_pkey PRIMARY KEY (id),
    CONSTRAINT equipment_equipment_location_id_fkey FOREIGN KEY (equipment_location_id) REFERENCES location_address (id)
);

--
-- Name: preparation_method_abbreviation; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS preparation_method_abbreviation (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT preparation_method_abbreviation_pkey PRIMARY KEY (id)
);

--
-- Name: preparation_method; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS preparation_method (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    name varchar,
    description varchar,
    prep_method_abbrev_id integer,
    prep_temp_c numeric,
    uri varchar,
    drying_step boolean,
    CONSTRAINT preparation_method_pkey PRIMARY KEY (id),
    CONSTRAINT preparation_method_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT preparation_method_prep_method_abbrev_id_fkey FOREIGN KEY (prep_method_abbrev_id) REFERENCES preparation_method_abbreviation (id)
);

--
-- Name: primary_ag_product; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS primary_ag_product (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT primary_ag_product_pkey PRIMARY KEY (id)
);

--
-- Name: processing_method; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS processing_method (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT processing_method_pkey PRIMARY KEY (id)
);

--
-- Name: provider; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS provider (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    codename varchar,
    CONSTRAINT provider_pkey PRIMARY KEY (id),
    CONSTRAINT provider_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id)
);

--
-- Name: resource_class; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS resource_class (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT resource_class_pkey PRIMARY KEY (id)
);

--
-- Name: resource_subclass; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS resource_subclass (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT resource_subclass_pkey PRIMARY KEY (id)
);

--
-- Name: resource; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS resource (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    name varchar,
    primary_ag_product_id integer,
    resource_class_id integer,
    resource_subclass_id integer,
    resource_code varchar,
    description varchar,
    CONSTRAINT resource_pkey PRIMARY KEY (id),
    CONSTRAINT resource_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT resource_primary_ag_product_id_fkey FOREIGN KEY (primary_ag_product_id) REFERENCES primary_ag_product (id),
    CONSTRAINT resource_resource_class_id_fkey FOREIGN KEY (resource_class_id) REFERENCES resource_class (id),
    CONSTRAINT resource_resource_subclass_id_fkey FOREIGN KEY (resource_subclass_id) REFERENCES resource_subclass (id)
);

--
-- Name: landiq_resource_mapping; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS landiq_resource_mapping (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    landiq_crop_name integer,
    resource_id integer,
    CONSTRAINT landiq_resource_mapping_pkey PRIMARY KEY (id),
    CONSTRAINT landiq_resource_mapping_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT landiq_resource_mapping_landiq_crop_name_fkey FOREIGN KEY (landiq_crop_name) REFERENCES primary_ag_product (id),
    CONSTRAINT landiq_resource_mapping_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);

--
-- Name: resource_availability; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS resource_availability (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    resource_id integer,
    geoid varchar,
    from_month integer,
    to_month integer,
    year_round boolean,
    residue_factor_dry_tons_acre double precision,
    residue_factor_wet_tons_acre double precision,
    note varchar,
    CONSTRAINT resource_availability_pkey PRIMARY KEY (id),
    CONSTRAINT resource_availability_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT resource_availability_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);

--
-- Name: resource_morphology; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS resource_morphology (
    id SERIAL,
    resource_id integer,
    morphology_uri varchar,
    CONSTRAINT resource_morphology_pkey PRIMARY KEY (id),
    CONSTRAINT resource_morphology_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);

--
-- Name: soil_type; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS soil_type (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT soil_type_pkey PRIMARY KEY (id)
);

--
-- Name: location_soil_type; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS location_soil_type (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    location_id integer,
    soil_type_id integer,
    CONSTRAINT location_soil_type_pkey PRIMARY KEY (id),
    CONSTRAINT location_soil_type_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT location_soil_type_location_id_fkey FOREIGN KEY (location_id) REFERENCES location_address (id),
    CONSTRAINT location_soil_type_soil_type_id_fkey FOREIGN KEY (soil_type_id) REFERENCES soil_type (id)
);

--
-- Name: source_type; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS source_type (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT source_type_pkey PRIMARY KEY (id)
);

--
-- Name: data_source_type; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS data_source_type (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    source_type_id integer,
    CONSTRAINT data_source_type_pkey PRIMARY KEY (id),
    CONSTRAINT data_source_type_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT data_source_type_source_type_id_fkey FOREIGN KEY (source_type_id) REFERENCES source_type (id)
);

--
-- Name: data_source; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS data_source (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    name varchar,
    description varchar,
    data_source_type_id integer,
    full_title varchar,
    creator varchar,
    subject varchar,
    publisher varchar,
    contributor varchar,
    date timestamp,
    type varchar,
    biocirv boolean,
    format varchar,
    language varchar,
    relation varchar,
    temporal_coverage varchar,
    location_coverage_id integer,
    rights varchar,
    license varchar,
    uri varchar,
    note varchar,
    CONSTRAINT data_source_pkey PRIMARY KEY (id),
    CONSTRAINT data_source_data_source_type_id_fkey FOREIGN KEY (data_source_type_id) REFERENCES data_source_type (id),
    CONSTRAINT data_source_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT data_source_location_coverage_id_fkey FOREIGN KEY (location_coverage_id) REFERENCES location_resolution (id)
);

--
-- Name: dataset; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS dataset (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    name varchar,
    record_type varchar,
    source_id integer,
    start_date date,
    end_date date,
    description varchar,
    CONSTRAINT dataset_pkey PRIMARY KEY (id),
    CONSTRAINT dataset_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT dataset_source_id_fkey FOREIGN KEY (source_id) REFERENCES data_source (id)
);

--
-- Name: facility_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS facility_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    dataset_id integer,
    facility_name varchar,
    location_id integer,
    capacity_mw numeric,
    resource_id integer,
    operator varchar,
    start_year integer,
    note varchar,
    CONSTRAINT facility_record_pkey PRIMARY KEY (id),
    CONSTRAINT facility_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT facility_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT facility_record_location_id_fkey FOREIGN KEY (location_id) REFERENCES location_address (id),
    CONSTRAINT facility_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);

--
-- Name: file_object_metadata; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS file_object_metadata (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    data_source_id integer,
    bucket_path varchar,
    file_format varchar,
    file_size integer,
    checksum_md5 varchar,
    checksum_sha256 varchar,
    CONSTRAINT file_object_metadata_pkey PRIMARY KEY (id),
    CONSTRAINT file_object_metadata_data_source_id_fkey FOREIGN KEY (data_source_id) REFERENCES data_source (id),
    CONSTRAINT file_object_metadata_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id)
);

--
-- Name: method; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS method (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    name varchar,
    method_abbrev_id integer,
    method_category_id integer,
    method_standard_id integer,
    description varchar,
    detection_limits varchar,
    source_id integer,
    CONSTRAINT method_pkey PRIMARY KEY (id),
    CONSTRAINT method_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT method_method_abbrev_id_fkey FOREIGN KEY (method_abbrev_id) REFERENCES method_abbrev (id),
    CONSTRAINT method_method_category_id_fkey FOREIGN KEY (method_category_id) REFERENCES method_category (id),
    CONSTRAINT method_method_standard_id_fkey FOREIGN KEY (method_standard_id) REFERENCES method_standard (id),
    CONSTRAINT method_source_id_fkey FOREIGN KEY (source_id) REFERENCES data_source (id)
);

--
-- Name: polygon; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS polygon (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    geoid varchar,
    geom geometry,
    dataset_id integer,
    CONSTRAINT polygon_pkey PRIMARY KEY (id),
    CONSTRAINT polygon_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT polygon_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id)
);

--
-- Name: idx_polygon_geom; Type: INDEX; Schema: -; Owner: -
--

CREATE INDEX IF NOT EXISTS idx_polygon_geom ON polygon USING gist (geom);

--
-- Name: unique_geom_dataset_md5; Type: INDEX; Schema: -; Owner: -
--

CREATE UNIQUE INDEX IF NOT EXISTS unique_geom_dataset_md5 ON polygon (md5(geom::text), dataset_id);

--
-- Name: landiq_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS landiq_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    record_id varchar NOT NULL,
    dataset_id integer,
    polygon_id integer,
    main_crop integer,
    secondary_crop integer,
    tertiary_crop integer,
    quaternary_crop integer,
    confidence integer,
    irrigated boolean,
    acres double precision,
    county varchar,
    version varchar,
    note varchar,
    pct1 double precision,
    pct2 double precision,
    pct3 double precision,
    pct4 double precision,
    CONSTRAINT landiq_record_pkey PRIMARY KEY (id),
    CONSTRAINT landiq_record_record_id_key UNIQUE (record_id),
    CONSTRAINT landiq_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT landiq_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT landiq_record_main_crop_fkey FOREIGN KEY (main_crop) REFERENCES primary_ag_product (id),
    CONSTRAINT landiq_record_polygon_id_fkey FOREIGN KEY (polygon_id) REFERENCES polygon (id),
    CONSTRAINT landiq_record_quaternary_crop_fkey FOREIGN KEY (quaternary_crop) REFERENCES primary_ag_product (id),
    CONSTRAINT landiq_record_secondary_crop_fkey FOREIGN KEY (secondary_crop) REFERENCES primary_ag_product (id),
    CONSTRAINT landiq_record_tertiary_crop_fkey FOREIGN KEY (tertiary_crop) REFERENCES primary_ag_product (id)
);

--
-- Name: spatial_ref_sys; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS spatial_ref_sys (
    srid integer,
    auth_name varchar(256),
    auth_srid integer,
    srtext varchar(2048),
    proj4text varchar(2048),
    CONSTRAINT spatial_ref_sys_pkey PRIMARY KEY (srid),
    CONSTRAINT spatial_ref_sys_srid_check CHECK (srid > 0 AND srid <= 998999)
);

--
-- Name: strain; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS strain (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    parent_strain_id integer,
    CONSTRAINT strain_pkey PRIMARY KEY (id)
);

--
-- Name: unit; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS unit (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT unit_pkey PRIMARY KEY (id)
);

--
-- Name: billion_ton2023_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS billion_ton2023_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    subclass_id integer,
    resource_id integer,
    geoid varchar,
    county_square_miles double precision,
    model_name varchar,
    scenario_name varchar,
    price_offered_usd numeric,
    production integer,
    production_unit_id integer,
    btu_ton integer,
    production_energy_content integer,
    energy_content_unit_id integer,
    product_density_dtpersqmi numeric,
    land_source varchar,
    CONSTRAINT billion_ton2023_record_pkey PRIMARY KEY (id),
    CONSTRAINT billion_ton2023_record_energy_content_unit_id_fkey FOREIGN KEY (energy_content_unit_id) REFERENCES unit (id),
    CONSTRAINT billion_ton2023_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT billion_ton2023_record_production_unit_id_fkey FOREIGN KEY (production_unit_id) REFERENCES unit (id),
    CONSTRAINT billion_ton2023_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id),
    CONSTRAINT billion_ton2023_record_subclass_id_fkey FOREIGN KEY (subclass_id) REFERENCES resource_subclass (id)
);

--
-- Name: experiment; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS experiment (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    analyst_id integer,
    exper_start_date date,
    exper_duration numeric,
    exper_duration_unit_id integer,
    exper_location_id integer,
    description varchar,
    CONSTRAINT experiment_pkey PRIMARY KEY (id),
    CONSTRAINT experiment_analyst_id_fkey FOREIGN KEY (analyst_id) REFERENCES contact (id),
    CONSTRAINT experiment_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT experiment_exper_duration_unit_id_fkey FOREIGN KEY (exper_duration_unit_id) REFERENCES unit (id),
    CONSTRAINT experiment_exper_location_id_fkey FOREIGN KEY (exper_location_id) REFERENCES location_address (id)
);

--
-- Name: experiment_analysis; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS experiment_analysis (
    id SERIAL,
    experiment_id integer,
    analysis_type_id integer,
    CONSTRAINT experiment_analysis_pkey PRIMARY KEY (id),
    CONSTRAINT experiment_analysis_analysis_type_id_fkey FOREIGN KEY (analysis_type_id) REFERENCES analysis_type (id),
    CONSTRAINT experiment_analysis_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id)
);

--
-- Name: experiment_equipment; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS experiment_equipment (
    id SERIAL,
    experiment_id integer,
    equipment_id integer,
    CONSTRAINT experiment_equipment_pkey PRIMARY KEY (id),
    CONSTRAINT experiment_equipment_equipment_id_fkey FOREIGN KEY (equipment_id) REFERENCES equipment (id),
    CONSTRAINT experiment_equipment_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id)
);

--
-- Name: experiment_method; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS experiment_method (
    id SERIAL,
    experiment_id integer,
    method_id integer,
    CONSTRAINT experiment_method_pkey PRIMARY KEY (id),
    CONSTRAINT experiment_method_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT experiment_method_method_id_fkey FOREIGN KEY (method_id) REFERENCES method (id)
);

--
-- Name: field_sample; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS field_sample (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    name varchar,
    resource_id integer,
    provider_id integer,
    collector_id integer,
    sample_collection_source varchar,
    amount_collected numeric,
    amount_collected_unit_id integer,
    sampling_location_id integer,
    field_storage_method_id integer,
    field_storage_duration_value numeric,
    field_storage_duration_unit_id integer,
    field_storage_location_id integer,
    collection_timestamp timestamp,
    collection_method_id integer,
    harvest_method_id integer,
    harvest_date date,
    field_sample_storage_location_id integer,
    note varchar,
    CONSTRAINT field_sample_pkey PRIMARY KEY (id),
    CONSTRAINT field_sample_amount_collected_unit_id_fkey FOREIGN KEY (amount_collected_unit_id) REFERENCES unit (id),
    CONSTRAINT field_sample_collection_method_id_fkey FOREIGN KEY (collection_method_id) REFERENCES collection_method (id),
    CONSTRAINT field_sample_collector_id_fkey FOREIGN KEY (collector_id) REFERENCES contact (id),
    CONSTRAINT field_sample_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT field_sample_field_sample_storage_location_id_fkey FOREIGN KEY (field_sample_storage_location_id) REFERENCES location_address (id),
    CONSTRAINT field_sample_field_storage_duration_unit_id_fkey FOREIGN KEY (field_storage_duration_unit_id) REFERENCES unit (id),
    CONSTRAINT field_sample_field_storage_location_id_fkey FOREIGN KEY (field_storage_location_id) REFERENCES location_address (id),
    CONSTRAINT field_sample_field_storage_method_id_fkey FOREIGN KEY (field_storage_method_id) REFERENCES field_storage_method (id),
    CONSTRAINT field_sample_harvest_method_id_fkey FOREIGN KEY (harvest_method_id) REFERENCES harvest_method (id),
    CONSTRAINT field_sample_provider_id_fkey FOREIGN KEY (provider_id) REFERENCES provider (id),
    CONSTRAINT field_sample_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id),
    CONSTRAINT field_sample_sampling_location_id_fkey FOREIGN KEY (sampling_location_id) REFERENCES location_address (id)
);

--
-- Name: field_sample_condition; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS field_sample_condition (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    field_sample_id integer,
    ag_treatment_id integer,
    last_application_date date,
    treatment_amount_per_acre double precision,
    processing_method_id integer,
    CONSTRAINT field_sample_condition_pkey PRIMARY KEY (id),
    CONSTRAINT field_sample_condition_ag_treatment_id_fkey FOREIGN KEY (ag_treatment_id) REFERENCES ag_treatment (id),
    CONSTRAINT field_sample_condition_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT field_sample_condition_field_sample_id_fkey FOREIGN KEY (field_sample_id) REFERENCES field_sample (id),
    CONSTRAINT field_sample_condition_processing_method_id_fkey FOREIGN KEY (processing_method_id) REFERENCES processing_method (id)
);

--
-- Name: parameter; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS parameter (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    name varchar,
    standard_unit_id integer,
    calculated boolean,
    description varchar,
    CONSTRAINT parameter_pkey PRIMARY KEY (id),
    CONSTRAINT parameter_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT parameter_standard_unit_id_fkey FOREIGN KEY (standard_unit_id) REFERENCES unit (id)
);

--
-- Name: observation; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS observation (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    record_id varchar NOT NULL,
    dataset_id integer,
    record_type varchar,
    parameter_id integer,
    value numeric,
    unit_id integer,
    dimension_type_id integer,
    dimension_value numeric,
    dimension_unit_id integer,
    note varchar,
    CONSTRAINT observation_pkey PRIMARY KEY (id),
    CONSTRAINT observation_record_id_key UNIQUE (record_id),
    CONSTRAINT observation_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT observation_dimension_type_id_fkey FOREIGN KEY (dimension_type_id) REFERENCES dimension_type (id),
    CONSTRAINT observation_dimension_unit_id_fkey FOREIGN KEY (dimension_unit_id) REFERENCES unit (id),
    CONSTRAINT observation_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT observation_parameter_id_fkey FOREIGN KEY (parameter_id) REFERENCES parameter (id),
    CONSTRAINT observation_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES unit (id)
);

--
-- Name: parameter_category_parameter; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS parameter_category_parameter (
    id SERIAL,
    parameter_id integer,
    parameter_category_id integer,
    CONSTRAINT parameter_category_parameter_pkey PRIMARY KEY (id),
    CONSTRAINT parameter_category_parameter_parameter_category_id_fkey FOREIGN KEY (parameter_category_id) REFERENCES parameter_category (id),
    CONSTRAINT parameter_category_parameter_parameter_id_fkey FOREIGN KEY (parameter_id) REFERENCES parameter (id)
);

--
-- Name: parameter_unit; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS parameter_unit (
    id SERIAL,
    parameter_id integer,
    alternate_unit_id integer,
    CONSTRAINT parameter_unit_pkey PRIMARY KEY (id),
    CONSTRAINT parameter_unit_alternate_unit_id_fkey FOREIGN KEY (alternate_unit_id) REFERENCES unit (id),
    CONSTRAINT parameter_unit_parameter_id_fkey FOREIGN KEY (parameter_id) REFERENCES parameter (id)
);

--
-- Name: physical_characteristic; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS physical_characteristic (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    field_sample_id integer,
    particle_length numeric,
    particle_width numeric,
    particle_height numeric,
    particle_unit_id integer,
    CONSTRAINT physical_characteristic_pkey PRIMARY KEY (id),
    CONSTRAINT physical_characteristic_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT physical_characteristic_field_sample_id_fkey FOREIGN KEY (field_sample_id) REFERENCES field_sample (id),
    CONSTRAINT physical_characteristic_particle_unit_id_fkey FOREIGN KEY (particle_unit_id) REFERENCES unit (id)
);

--
-- Name: prepared_sample; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS prepared_sample (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    name varchar,
    field_sample_id integer,
    prep_method_id integer,
    prep_date date,
    preparer_id integer,
    note varchar,
    CONSTRAINT prepared_sample_pkey PRIMARY KEY (id),
    CONSTRAINT prepared_sample_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT prepared_sample_field_sample_id_fkey FOREIGN KEY (field_sample_id) REFERENCES field_sample (id),
    CONSTRAINT prepared_sample_prep_method_id_fkey FOREIGN KEY (prep_method_id) REFERENCES preparation_method (id),
    CONSTRAINT prepared_sample_preparer_id_fkey FOREIGN KEY (preparer_id) REFERENCES contact (id)
);

--
-- Name: autoclave_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS autoclave_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    record_id varchar NOT NULL,
    dataset_id integer,
    experiment_id integer,
    resource_id integer,
    prepared_sample_id integer,
    technical_replicate_no integer,
    technical_replicate_total integer,
    method_id integer,
    analyst_id integer,
    raw_data_id integer,
    qc_pass varchar,
    note varchar,
    CONSTRAINT autoclave_record_pkey PRIMARY KEY (id),
    CONSTRAINT autoclave_record_record_id_key UNIQUE (record_id),
    CONSTRAINT autoclave_record_analyst_id_fkey FOREIGN KEY (analyst_id) REFERENCES contact (id),
    CONSTRAINT autoclave_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT autoclave_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT autoclave_record_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT autoclave_record_method_id_fkey FOREIGN KEY (method_id) REFERENCES method (id),
    CONSTRAINT autoclave_record_prepared_sample_id_fkey FOREIGN KEY (prepared_sample_id) REFERENCES prepared_sample (id),
    CONSTRAINT autoclave_record_raw_data_id_fkey FOREIGN KEY (raw_data_id) REFERENCES file_object_metadata (id),
    CONSTRAINT autoclave_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);

--
-- Name: calorimetry_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS calorimetry_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    record_id varchar NOT NULL,
    dataset_id integer,
    experiment_id integer,
    resource_id integer,
    prepared_sample_id integer,
    technical_replicate_no integer,
    technical_replicate_total integer,
    method_id integer,
    analyst_id integer,
    raw_data_id integer,
    qc_pass varchar,
    note varchar,
    CONSTRAINT calorimetry_record_pkey PRIMARY KEY (id),
    CONSTRAINT calorimetry_record_record_id_key UNIQUE (record_id),
    CONSTRAINT calorimetry_record_analyst_id_fkey FOREIGN KEY (analyst_id) REFERENCES contact (id),
    CONSTRAINT calorimetry_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT calorimetry_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT calorimetry_record_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT calorimetry_record_method_id_fkey FOREIGN KEY (method_id) REFERENCES method (id),
    CONSTRAINT calorimetry_record_prepared_sample_id_fkey FOREIGN KEY (prepared_sample_id) REFERENCES prepared_sample (id),
    CONSTRAINT calorimetry_record_raw_data_id_fkey FOREIGN KEY (raw_data_id) REFERENCES file_object_metadata (id),
    CONSTRAINT calorimetry_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);

--
-- Name: compositional_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS compositional_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    record_id varchar NOT NULL,
    dataset_id integer,
    experiment_id integer,
    resource_id integer,
    prepared_sample_id integer,
    technical_replicate_no integer,
    technical_replicate_total integer,
    method_id integer,
    analyst_id integer,
    raw_data_id integer,
    qc_pass varchar,
    note varchar,
    CONSTRAINT compositional_record_pkey PRIMARY KEY (id),
    CONSTRAINT compositional_record_record_id_key UNIQUE (record_id),
    CONSTRAINT compositional_record_analyst_id_fkey FOREIGN KEY (analyst_id) REFERENCES contact (id),
    CONSTRAINT compositional_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT compositional_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT compositional_record_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT compositional_record_method_id_fkey FOREIGN KEY (method_id) REFERENCES method (id),
    CONSTRAINT compositional_record_prepared_sample_id_fkey FOREIGN KEY (prepared_sample_id) REFERENCES prepared_sample (id),
    CONSTRAINT compositional_record_raw_data_id_fkey FOREIGN KEY (raw_data_id) REFERENCES file_object_metadata (id),
    CONSTRAINT compositional_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);

--
-- Name: experiment_prepared_sample; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS experiment_prepared_sample (
    id SERIAL,
    experiment_id integer,
    prepared_sample_id integer,
    CONSTRAINT experiment_prepared_sample_pkey PRIMARY KEY (id),
    CONSTRAINT experiment_prepared_sample_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT experiment_prepared_sample_prepared_sample_id_fkey FOREIGN KEY (prepared_sample_id) REFERENCES prepared_sample (id)
);

--
-- Name: fermentation_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS fermentation_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    record_id varchar NOT NULL,
    dataset_id integer,
    experiment_id integer,
    resource_id integer,
    prepared_sample_id integer,
    technical_replicate_no integer,
    technical_replicate_total integer,
    method_id integer,
    analyst_id integer,
    raw_data_id integer,
    qc_pass varchar,
    note varchar,
    strain_id integer,
    pretreatment_method_id integer,
    eh_method_id integer,
    well_position varchar,
    temperature numeric,
    agitation_rpm numeric,
    vessel_id integer,
    analyte_detection_equipment_id integer,
    CONSTRAINT fermentation_record_pkey PRIMARY KEY (id),
    CONSTRAINT fermentation_record_record_id_key UNIQUE (record_id),
    CONSTRAINT fermentation_record_analyst_id_fkey FOREIGN KEY (analyst_id) REFERENCES contact (id),
    CONSTRAINT fermentation_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT fermentation_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT fermentation_record_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT fermentation_record_method_id_fkey FOREIGN KEY (method_id) REFERENCES method (id),
    CONSTRAINT fermentation_record_prepared_sample_id_fkey FOREIGN KEY (prepared_sample_id) REFERENCES prepared_sample (id),
    CONSTRAINT fermentation_record_raw_data_id_fkey FOREIGN KEY (raw_data_id) REFERENCES file_object_metadata (id),
    CONSTRAINT fermentation_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);

--
-- Name: ftnir_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS ftnir_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    record_id varchar NOT NULL,
    dataset_id integer,
    experiment_id integer,
    resource_id integer,
    prepared_sample_id integer,
    technical_replicate_no integer,
    technical_replicate_total integer,
    method_id integer,
    analyst_id integer,
    raw_data_id integer,
    qc_pass varchar,
    note varchar,
    CONSTRAINT ftnir_record_pkey PRIMARY KEY (id),
    CONSTRAINT ftnir_record_record_id_key UNIQUE (record_id),
    CONSTRAINT ftnir_record_analyst_id_fkey FOREIGN KEY (analyst_id) REFERENCES contact (id),
    CONSTRAINT ftnir_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT ftnir_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT ftnir_record_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT ftnir_record_method_id_fkey FOREIGN KEY (method_id) REFERENCES method (id),
    CONSTRAINT ftnir_record_prepared_sample_id_fkey FOREIGN KEY (prepared_sample_id) REFERENCES prepared_sample (id),
    CONSTRAINT ftnir_record_raw_data_id_fkey FOREIGN KEY (raw_data_id) REFERENCES file_object_metadata (id),
    CONSTRAINT ftnir_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);

--
-- Name: gasification_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS gasification_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    record_id varchar NOT NULL,
    dataset_id integer,
    experiment_id integer,
    resource_id integer,
    prepared_sample_id integer,
    technical_replicate_no integer,
    technical_replicate_total integer,
    method_id integer,
    analyst_id integer,
    raw_data_id integer,
    qc_pass varchar,
    note varchar,
    feedstock_mass numeric,
    bed_temperature numeric,
    gas_flow_rate numeric,
    CONSTRAINT gasification_record_pkey PRIMARY KEY (id),
    CONSTRAINT gasification_record_record_id_key UNIQUE (record_id),
    CONSTRAINT gasification_record_analyst_id_fkey FOREIGN KEY (analyst_id) REFERENCES contact (id),
    CONSTRAINT gasification_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT gasification_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT gasification_record_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT gasification_record_method_id_fkey FOREIGN KEY (method_id) REFERENCES method (id),
    CONSTRAINT gasification_record_prepared_sample_id_fkey FOREIGN KEY (prepared_sample_id) REFERENCES prepared_sample (id),
    CONSTRAINT gasification_record_raw_data_id_fkey FOREIGN KEY (raw_data_id) REFERENCES file_object_metadata (id),
    CONSTRAINT gasification_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);

--
-- Name: icp_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS icp_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    record_id varchar NOT NULL,
    dataset_id integer,
    experiment_id integer,
    resource_id integer,
    prepared_sample_id integer,
    technical_replicate_no integer,
    technical_replicate_total integer,
    method_id integer,
    analyst_id integer,
    raw_data_id integer,
    qc_pass varchar,
    note varchar,
    CONSTRAINT icp_record_pkey PRIMARY KEY (id),
    CONSTRAINT icp_record_record_id_key UNIQUE (record_id),
    CONSTRAINT icp_record_analyst_id_fkey FOREIGN KEY (analyst_id) REFERENCES contact (id),
    CONSTRAINT icp_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT icp_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT icp_record_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT icp_record_method_id_fkey FOREIGN KEY (method_id) REFERENCES method (id),
    CONSTRAINT icp_record_prepared_sample_id_fkey FOREIGN KEY (prepared_sample_id) REFERENCES prepared_sample (id),
    CONSTRAINT icp_record_raw_data_id_fkey FOREIGN KEY (raw_data_id) REFERENCES file_object_metadata (id),
    CONSTRAINT icp_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);

--
-- Name: pretreatment_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS pretreatment_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    record_id varchar NOT NULL,
    dataset_id integer,
    experiment_id integer,
    resource_id integer,
    prepared_sample_id integer,
    technical_replicate_no integer,
    technical_replicate_total integer,
    method_id integer,
    analyst_id integer,
    raw_data_id integer,
    qc_pass varchar,
    note varchar,
    pretreatment_method_id integer,
    eh_method_id integer,
    reaction_block_id integer,
    block_position varchar,
    temperature numeric,
    replicate_no integer,
    CONSTRAINT pretreatment_record_pkey PRIMARY KEY (id),
    CONSTRAINT pretreatment_record_record_id_key UNIQUE (record_id),
    CONSTRAINT pretreatment_record_analyst_id_fkey FOREIGN KEY (analyst_id) REFERENCES contact (id),
    CONSTRAINT pretreatment_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT pretreatment_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT pretreatment_record_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT pretreatment_record_method_id_fkey FOREIGN KEY (method_id) REFERENCES method (id),
    CONSTRAINT pretreatment_record_prepared_sample_id_fkey FOREIGN KEY (prepared_sample_id) REFERENCES prepared_sample (id),
    CONSTRAINT pretreatment_record_raw_data_id_fkey FOREIGN KEY (raw_data_id) REFERENCES file_object_metadata (id),
    CONSTRAINT pretreatment_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);

--
-- Name: proximate_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS proximate_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    record_id varchar NOT NULL,
    dataset_id integer,
    experiment_id integer,
    resource_id integer,
    prepared_sample_id integer,
    technical_replicate_no integer,
    technical_replicate_total integer,
    method_id integer,
    analyst_id integer,
    raw_data_id integer,
    qc_pass varchar,
    note varchar,
    CONSTRAINT proximate_record_pkey PRIMARY KEY (id),
    CONSTRAINT proximate_record_record_id_key UNIQUE (record_id),
    CONSTRAINT proximate_record_analyst_id_fkey FOREIGN KEY (analyst_id) REFERENCES contact (id),
    CONSTRAINT proximate_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT proximate_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT proximate_record_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT proximate_record_method_id_fkey FOREIGN KEY (method_id) REFERENCES method (id),
    CONSTRAINT proximate_record_prepared_sample_id_fkey FOREIGN KEY (prepared_sample_id) REFERENCES prepared_sample (id),
    CONSTRAINT proximate_record_raw_data_id_fkey FOREIGN KEY (raw_data_id) REFERENCES file_object_metadata (id),
    CONSTRAINT proximate_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);

--
-- Name: rgb_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS rgb_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    record_id varchar NOT NULL,
    dataset_id integer,
    experiment_id integer,
    resource_id integer,
    prepared_sample_id integer,
    technical_replicate_no integer,
    technical_replicate_total integer,
    method_id integer,
    analyst_id integer,
    raw_data_id integer,
    qc_pass varchar,
    note varchar,
    CONSTRAINT rgb_record_pkey PRIMARY KEY (id),
    CONSTRAINT rgb_record_record_id_key UNIQUE (record_id),
    CONSTRAINT rgb_record_analyst_id_fkey FOREIGN KEY (analyst_id) REFERENCES contact (id),
    CONSTRAINT rgb_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT rgb_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT rgb_record_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT rgb_record_method_id_fkey FOREIGN KEY (method_id) REFERENCES method (id),
    CONSTRAINT rgb_record_prepared_sample_id_fkey FOREIGN KEY (prepared_sample_id) REFERENCES prepared_sample (id),
    CONSTRAINT rgb_record_raw_data_id_fkey FOREIGN KEY (raw_data_id) REFERENCES file_object_metadata (id),
    CONSTRAINT rgb_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);

--
-- Name: ultimate_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS ultimate_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    record_id varchar NOT NULL,
    dataset_id integer,
    experiment_id integer,
    resource_id integer,
    prepared_sample_id integer,
    technical_replicate_no integer,
    technical_replicate_total integer,
    method_id integer,
    analyst_id integer,
    raw_data_id integer,
    qc_pass varchar,
    note varchar,
    CONSTRAINT ultimate_record_pkey PRIMARY KEY (id),
    CONSTRAINT ultimate_record_record_id_key UNIQUE (record_id),
    CONSTRAINT ultimate_record_analyst_id_fkey FOREIGN KEY (analyst_id) REFERENCES contact (id),
    CONSTRAINT ultimate_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT ultimate_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT ultimate_record_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT ultimate_record_method_id_fkey FOREIGN KEY (method_id) REFERENCES method (id),
    CONSTRAINT ultimate_record_prepared_sample_id_fkey FOREIGN KEY (prepared_sample_id) REFERENCES prepared_sample (id),
    CONSTRAINT ultimate_record_raw_data_id_fkey FOREIGN KEY (raw_data_id) REFERENCES file_object_metadata (id),
    CONSTRAINT ultimate_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);

--
-- Name: usda_commodity; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_commodity (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    usda_source varchar,
    usda_code varchar,
    parent_commodity_id integer,
    CONSTRAINT usda_commodity_pkey PRIMARY KEY (id),
    CONSTRAINT usda_commodity_parent_commodity_id_fkey FOREIGN KEY (parent_commodity_id) REFERENCES usda_commodity (id)
);

--
-- Name: resource_usda_commodity_map; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS resource_usda_commodity_map (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    resource_id integer,
    primary_ag_product_id integer,
    usda_commodity_id integer,
    match_tier varchar,
    note varchar,
    CONSTRAINT resource_usda_commodity_map_pkey PRIMARY KEY (id),
    CONSTRAINT resource_usda_commodity_map_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT resource_usda_commodity_map_primary_ag_product_id_fkey FOREIGN KEY (primary_ag_product_id) REFERENCES primary_ag_product (id),
    CONSTRAINT resource_usda_commodity_map_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id),
    CONSTRAINT resource_usda_commodity_map_usda_commodity_id_fkey FOREIGN KEY (usda_commodity_id) REFERENCES usda_commodity (id)
);

--
-- Name: usda_census_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_census_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    dataset_id integer,
    geoid varchar,
    commodity_code integer,
    year integer,
    source_reference varchar,
    note varchar,
    CONSTRAINT usda_census_record_pkey PRIMARY KEY (id),
    CONSTRAINT usda_census_record_commodity_code_fkey FOREIGN KEY (commodity_code) REFERENCES usda_commodity (id),
    CONSTRAINT usda_census_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT usda_census_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id)
);

--
-- Name: usda_domain; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_domain (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT usda_domain_pkey PRIMARY KEY (id)
);

--
-- Name: usda_market_report; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_market_report (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    slug_id integer,
    slug_name varchar,
    report_series_title varchar,
    frequency varchar,
    office_name varchar,
    office_city_id integer,
    office_state_fips varchar,
    source_id integer,
    CONSTRAINT usda_market_report_pkey PRIMARY KEY (id),
    CONSTRAINT usda_market_report_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT usda_market_report_office_city_id_fkey FOREIGN KEY (office_city_id) REFERENCES location_address (id),
    CONSTRAINT usda_market_report_source_id_fkey FOREIGN KEY (source_id) REFERENCES data_source (id)
);

--
-- Name: usda_market_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_market_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    report_id integer,
    dataset_id integer,
    report_begin_date timestamp,
    report_end_date timestamp,
    report_date timestamp,
    commodity_id integer,
    market_type_id integer,
    market_type_category varchar,
    grp varchar,
    market_category_id integer,
    class_ varchar,
    grade varchar,
    variety varchar,
    protein_pct numeric,
    application varchar,
    pkg varchar,
    sale_type varchar,
    price_unit_id integer,
    freight varchar,
    trans_mode varchar,
    CONSTRAINT usda_market_record_pkey PRIMARY KEY (id),
    CONSTRAINT usda_market_record_commodity_id_fkey FOREIGN KEY (commodity_id) REFERENCES usda_commodity (id),
    CONSTRAINT usda_market_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT usda_market_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT usda_market_record_price_unit_id_fkey FOREIGN KEY (price_unit_id) REFERENCES unit (id),
    CONSTRAINT usda_market_record_report_id_fkey FOREIGN KEY (report_id) REFERENCES usda_market_report (id)
);

--
-- Name: usda_statistic_category; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_statistic_category (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT usda_statistic_category_pkey PRIMARY KEY (id)
);

--
-- Name: usda_survey_program; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_survey_program (
    id SERIAL,
    name varchar,
    description varchar,
    uri varchar,
    CONSTRAINT usda_survey_program_pkey PRIMARY KEY (id)
);

--
-- Name: usda_survey_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_survey_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    dataset_id integer,
    geoid varchar,
    commodity_code integer,
    year integer,
    survey_program_id integer,
    survey_period varchar,
    reference_month varchar,
    seasonal_flag boolean,
    note varchar,
    CONSTRAINT usda_survey_record_pkey PRIMARY KEY (id),
    CONSTRAINT usda_survey_record_commodity_code_fkey FOREIGN KEY (commodity_code) REFERENCES usda_commodity (id),
    CONSTRAINT usda_survey_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT usda_survey_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT usda_survey_record_survey_program_id_fkey FOREIGN KEY (survey_program_id) REFERENCES usda_survey_program (id)
);

--
-- Name: usda_term_map; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_term_map (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    source_system varchar,
    source_context varchar,
    raw_term varchar,
    usda_commodity_id integer,
    is_verified boolean,
    note varchar,
    CONSTRAINT usda_term_map_pkey PRIMARY KEY (id),
    CONSTRAINT usda_term_map_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT usda_term_map_usda_commodity_id_fkey FOREIGN KEY (usda_commodity_id) REFERENCES usda_commodity (id)
);

--
-- Name: xrd_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS xrd_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    record_id varchar NOT NULL,
    dataset_id integer,
    experiment_id integer,
    resource_id integer,
    prepared_sample_id integer,
    technical_replicate_no integer,
    technical_replicate_total integer,
    method_id integer,
    analyst_id integer,
    raw_data_id integer,
    qc_pass varchar,
    note varchar,
    scan_low_nm integer,
    scan_high_nm integer,
    CONSTRAINT xrd_record_pkey PRIMARY KEY (id),
    CONSTRAINT xrd_record_record_id_key UNIQUE (record_id),
    CONSTRAINT xrd_record_analyst_id_fkey FOREIGN KEY (analyst_id) REFERENCES contact (id),
    CONSTRAINT xrd_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT xrd_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT xrd_record_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT xrd_record_method_id_fkey FOREIGN KEY (method_id) REFERENCES method (id),
    CONSTRAINT xrd_record_prepared_sample_id_fkey FOREIGN KEY (prepared_sample_id) REFERENCES prepared_sample (id),
    CONSTRAINT xrd_record_raw_data_id_fkey FOREIGN KEY (raw_data_id) REFERENCES file_object_metadata (id),
    CONSTRAINT xrd_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);

--
-- Name: xrf_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS xrf_record (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    record_id varchar NOT NULL,
    dataset_id integer,
    experiment_id integer,
    resource_id integer,
    prepared_sample_id integer,
    technical_replicate_no integer,
    technical_replicate_total integer,
    method_id integer,
    analyst_id integer,
    raw_data_id integer,
    qc_pass varchar,
    note varchar,
    wavelength_nm numeric,
    intensity numeric,
    energy_slope numeric,
    energy_offset numeric,
    CONSTRAINT xrf_record_pkey PRIMARY KEY (id),
    CONSTRAINT xrf_record_record_id_key UNIQUE (record_id),
    CONSTRAINT xrf_record_analyst_id_fkey FOREIGN KEY (analyst_id) REFERENCES contact (id),
    CONSTRAINT xrf_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT xrf_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT xrf_record_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT xrf_record_method_id_fkey FOREIGN KEY (method_id) REFERENCES method (id),
    CONSTRAINT xrf_record_prepared_sample_id_fkey FOREIGN KEY (prepared_sample_id) REFERENCES prepared_sample (id),
    CONSTRAINT xrf_record_raw_data_id_fkey FOREIGN KEY (raw_data_id) REFERENCES file_object_metadata (id),
    CONSTRAINT xrf_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);

--
-- Name: geography_columns; Type: VIEW; Schema: -; Owner: -
--

CREATE OR REPLACE VIEW geography_columns AS
 SELECT current_database() AS f_table_catalog,
    n.nspname AS f_table_schema,
    c.relname AS f_table_name,
    a.attname AS f_geography_column,
    postgis_typmod_dims(a.atttypmod) AS coord_dimension,
    postgis_typmod_srid(a.atttypmod) AS srid,
    postgis_typmod_type(a.atttypmod) AS type
   FROM pg_class c,
    pg_attribute a,
    pg_type t,
    pg_namespace n
  WHERE t.typname = 'geography'::name AND a.attisdropped = false AND a.atttypid = t.oid AND a.attrelid = c.oid AND c.relnamespace = n.oid AND (c.relkind = ANY (ARRAY['r'::"char", 'v'::"char", 'm'::"char", 'f'::"char", 'p'::"char"])) AND NOT pg_is_other_temp_schema(c.relnamespace) AND has_table_privilege(c.oid, 'SELECT'::text);

--
-- Name: geometry_columns; Type: VIEW; Schema: -; Owner: -
--

CREATE OR REPLACE VIEW geometry_columns AS
 SELECT current_database()::character varying(256) AS f_table_catalog,
    n.nspname AS f_table_schema,
    c.relname AS f_table_name,
    a.attname AS f_geometry_column,
    COALESCE(postgis_typmod_dims(a.atttypmod), sn.ndims, 2) AS coord_dimension,
    COALESCE(NULLIF(postgis_typmod_srid(a.atttypmod), 0), sr.srid, 0) AS srid,
    replace(replace(COALESCE(NULLIF(upper(postgis_typmod_type(a.atttypmod)), 'GEOMETRY'::text), st.type, 'GEOMETRY'::text), 'ZM'::text, ''::text), 'Z'::text, ''::text)::character varying(30) AS type
   FROM pg_class c
     JOIN pg_attribute a ON a.attrelid = c.oid AND NOT a.attisdropped
     JOIN pg_namespace n ON c.relnamespace = n.oid
     JOIN pg_type t ON a.atttypid = t.oid
     LEFT JOIN ( SELECT s.connamespace,
            s.conrelid,
            s.conkey,
            replace(split_part(s.consrc, ''''::text, 2), ')'::text, ''::text) AS type
           FROM ( SELECT pg_constraint.connamespace,
                    pg_constraint.conrelid,
                    pg_constraint.conkey,
                    pg_get_constraintdef(pg_constraint.oid) AS consrc
                   FROM pg_constraint) s
          WHERE s.consrc ~~* '%geometrytype(% = %'::text) st ON st.connamespace = n.oid AND st.conrelid = c.oid AND (a.attnum = ANY (st.conkey))
     LEFT JOIN ( SELECT s.connamespace,
            s.conrelid,
            s.conkey,
            replace(split_part(s.consrc, ' = '::text, 2), ')'::text, ''::text)::integer AS ndims
           FROM ( SELECT pg_constraint.connamespace,
                    pg_constraint.conrelid,
                    pg_constraint.conkey,
                    pg_get_constraintdef(pg_constraint.oid) AS consrc
                   FROM pg_constraint) s
          WHERE s.consrc ~~* '%ndims(% = %'::text) sn ON sn.connamespace = n.oid AND sn.conrelid = c.oid AND (a.attnum = ANY (sn.conkey))
     LEFT JOIN ( SELECT s.connamespace,
            s.conrelid,
            s.conkey,
            replace(replace(split_part(s.consrc, ' = '::text, 2), ')'::text, ''::text), '('::text, ''::text)::integer AS srid
           FROM ( SELECT pg_constraint.connamespace,
                    pg_constraint.conrelid,
                    pg_constraint.conkey,
                    pg_get_constraintdef(pg_constraint.oid) AS consrc
                   FROM pg_constraint) s
          WHERE s.consrc ~~* '%srid(% = %'::text) sr ON sr.connamespace = n.oid AND sr.conrelid = c.oid AND (a.attnum = ANY (sr.conkey))
  WHERE (c.relkind = ANY (ARRAY['r'::"char", 'v'::"char", 'm'::"char", 'f'::"char", 'p'::"char"])) AND NOT c.relname = 'raster_columns'::name AND t.typname = 'geometry'::name AND NOT pg_is_other_temp_schema(c.relnamespace) AND has_table_privilege(c.oid, 'SELECT'::text);

--
-- Name: spatial_ref_sys; Type: PRIVILEGE; Schema: privileges; Owner: -
--

GRANT SELECT ON TABLE spatial_ref_sys TO PUBLIC;

--
-- Name: geography_columns; Type: PRIVILEGE; Schema: privileges; Owner: -
--

GRANT SELECT ON TABLE geography_columns TO PUBLIC;

--
-- Name: geometry_columns; Type: PRIVILEGE; Schema: privileges; Owner: -
--

GRANT SELECT ON TABLE geometry_columns TO PUBLIC;
