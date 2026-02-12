--
-- Name: resource_availability; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS resource_availability (
    resource_id integer,
    geoid text,
    from_month integer,
    to_month integer,
    year_round boolean,
    note text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    residue_factor_dry_tons_acre double precision,
    residue_factor_wet_tons_acre double precision,
    CONSTRAINT resource_availability_pkey PRIMARY KEY (id),
    CONSTRAINT resource_availability_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT resource_availability_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);
