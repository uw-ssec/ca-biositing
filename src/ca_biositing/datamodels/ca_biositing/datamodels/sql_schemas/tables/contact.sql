
--
-- Name: contact; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS contact (
    first_name text,
    last_name text,
    email text,
    affiliation text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    name text,
    middle_name text,
    CONSTRAINT contact_pkey PRIMARY KEY (id),
    CONSTRAINT contact_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id)
);
