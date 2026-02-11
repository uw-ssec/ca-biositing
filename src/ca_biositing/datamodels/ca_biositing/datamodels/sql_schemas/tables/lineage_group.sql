--
-- Name: lineage_group; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS lineage_group (
    id SERIAL,
    etl_run_id integer,
    note text,
    CONSTRAINT lineage_group_pkey PRIMARY KEY (id),
    CONSTRAINT lineage_group_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id)
);
