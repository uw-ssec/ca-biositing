--
-- Name: data_source_type; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS data_source_type (
    source_type_id integer,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT data_source_type_pkey PRIMARY KEY (id),
    CONSTRAINT data_source_type_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT data_source_type_source_type_id_fkey FOREIGN KEY (source_type_id) REFERENCES source_type (id)
);
