--
-- Name: method; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS method (
    name text,
    method_abbrev_id integer,
    method_category_id integer,
    method_standard_id integer,
    description text,
    detection_limits text,
    source_id integer,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT method_pkey PRIMARY KEY (id),
    CONSTRAINT method_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT method_method_abbrev_id_fkey FOREIGN KEY (method_abbrev_id) REFERENCES method_abbrev (id),
    CONSTRAINT method_method_category_id_fkey FOREIGN KEY (method_category_id) REFERENCES method_category (id),
    CONSTRAINT method_method_standard_id_fkey FOREIGN KEY (method_standard_id) REFERENCES method_standard (id),
    CONSTRAINT method_source_id_fkey FOREIGN KEY (source_id) REFERENCES data_source (id)
);
