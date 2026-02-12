--
-- Name: base_entity; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS base_entity (
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT base_entity_pkey PRIMARY KEY (id),
    CONSTRAINT base_entity_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id)
);
