--
-- Name: parameter; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS parameter (
    name text,
    standard_unit_id integer,
    calculated boolean,
    description text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT parameter_pkey PRIMARY KEY (id),
    CONSTRAINT parameter_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT parameter_standard_unit_id_fkey FOREIGN KEY (standard_unit_id) REFERENCES unit (id)
);
