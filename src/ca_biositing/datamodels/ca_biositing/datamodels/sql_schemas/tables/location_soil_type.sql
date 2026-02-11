--
-- Name: location_soil_type; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS location_soil_type (
    location_id integer,
    soil_type_id integer,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT location_soil_type_pkey PRIMARY KEY (id),
    CONSTRAINT location_soil_type_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT location_soil_type_location_id_fkey FOREIGN KEY (location_id) REFERENCES location_address (id),
    CONSTRAINT location_soil_type_soil_type_id_fkey FOREIGN KEY (soil_type_id) REFERENCES soil_type (id)
);
