--
-- Name: billion_ton2023_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS billion_ton2023_record (
    subclass_id integer,
    resource_id integer,
    geoid text,
    county_square_miles double precision,
    model_name text,
    scenario_name text,
    price_offered_usd numeric,
    production integer,
    production_unit_id integer,
    btu_ton integer,
    production_energy_content integer,
    energy_content_unit_id integer,
    product_density_dtpersqmi numeric,
    land_source text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT billion_ton2023_record_pkey PRIMARY KEY (id),
    CONSTRAINT billion_ton2023_record_energy_content_unit_id_fkey FOREIGN KEY (energy_content_unit_id) REFERENCES unit (id),
    CONSTRAINT billion_ton2023_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT billion_ton2023_record_production_unit_id_fkey FOREIGN KEY (production_unit_id) REFERENCES unit (id),
    CONSTRAINT billion_ton2023_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id),
    CONSTRAINT billion_ton2023_record_subclass_id_fkey FOREIGN KEY (subclass_id) REFERENCES resource_subclass (id)
);
