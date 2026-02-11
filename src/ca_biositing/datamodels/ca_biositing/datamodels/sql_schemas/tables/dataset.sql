--
-- Name: dataset; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS dataset (
    name text,
    record_type text,
    source_id integer,
    start_date date,
    end_date date,
    description text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT dataset_pkey PRIMARY KEY (id),
    CONSTRAINT dataset_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT dataset_source_id_fkey FOREIGN KEY (source_id) REFERENCES data_source (id)
);
