--
-- Name: preparation_method; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS preparation_method (
    name text,
    description text,
    prep_method_abbrev_id integer,
    prep_temp_c numeric,
    uri text,
    drying_step boolean,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT preparation_method_pkey PRIMARY KEY (id),
    CONSTRAINT preparation_method_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT preparation_method_prep_method_abbrev_id_fkey FOREIGN KEY (prep_method_abbrev_id) REFERENCES preparation_method_abbreviation (id)
);
