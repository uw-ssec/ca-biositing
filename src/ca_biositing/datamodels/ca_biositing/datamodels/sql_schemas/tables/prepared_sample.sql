--
-- Name: prepared_sample; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS prepared_sample (
    name text,
    field_sample_id integer,
    prep_method_id integer,
    prep_date date,
    preparer_id integer,
    note text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT prepared_sample_pkey PRIMARY KEY (id),
    CONSTRAINT prepared_sample_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT prepared_sample_field_sample_id_fkey FOREIGN KEY (field_sample_id) REFERENCES field_sample (id),
    CONSTRAINT prepared_sample_prep_method_id_fkey FOREIGN KEY (prep_method_id) REFERENCES preparation_method (id),
    CONSTRAINT prepared_sample_preparer_id_fkey FOREIGN KEY (preparer_id) REFERENCES contact (id)
);
