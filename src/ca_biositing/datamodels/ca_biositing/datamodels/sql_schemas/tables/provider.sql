--
-- Name: provider; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS provider (
    codename text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT provider_pkey PRIMARY KEY (id),
    CONSTRAINT provider_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id)
);
