--
-- Name: etl_run; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS etl_run (
    id SERIAL,
    run_id text,
    started_at timestamp,
    completed_at timestamp,
    pipeline_name text,
    status text,
    records_ingested integer,
    note text,
    CONSTRAINT etl_run_pkey PRIMARY KEY (id)
);
