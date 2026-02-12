--
-- Name: data_source; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS data_source (
    name text,
    description text,
    data_source_type_id integer,
    full_title text,
    creator text,
    subject text,
    publisher text,
    contributor text,
    date timestamp,
    type text,
    biocirv boolean,
    format text,
    language text,
    relation text,
    temporal_coverage text,
    location_coverage_id integer,
    rights text,
    license text,
    uri text,
    note text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT data_source_pkey PRIMARY KEY (id),
    CONSTRAINT data_source_data_source_type_id_fkey FOREIGN KEY (data_source_type_id) REFERENCES data_source_type (id),
    CONSTRAINT data_source_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT data_source_location_coverage_id_fkey FOREIGN KEY (location_coverage_id) REFERENCES location_resolution (id)
);
