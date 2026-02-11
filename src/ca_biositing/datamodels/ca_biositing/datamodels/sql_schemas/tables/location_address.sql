--
-- Name: location_address; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS location_address (
    geography_id text,
    address_line1 text,
    address_line2 text,
    city text,
    zip text,
    lat double precision,
    lon double precision,
    is_anonymous boolean,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT location_address_pkey PRIMARY KEY (id),
    CONSTRAINT location_address_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT location_address_geography_id_fkey FOREIGN KEY (geography_id) REFERENCES place (geoid)
);
