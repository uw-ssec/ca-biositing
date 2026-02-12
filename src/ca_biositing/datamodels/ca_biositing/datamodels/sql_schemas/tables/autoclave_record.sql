--
-- Name: autoclave_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS autoclave_record (
    record_id text NOT NULL,
    dataset_id integer,
    experiment_id integer,
    resource_id integer,
    prepared_sample_id integer,
    technical_replicate_no integer,
    technical_replicate_total integer,
    method_id integer,
    analyst_id integer,
    raw_data_id integer,
    qc_pass text,
    note text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT autoclave_record_pkey PRIMARY KEY (id),
    CONSTRAINT autoclave_record_record_id_key UNIQUE (record_id),
    CONSTRAINT autoclave_record_analyst_id_fkey FOREIGN KEY (analyst_id) REFERENCES contact (id),
    CONSTRAINT autoclave_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT autoclave_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT autoclave_record_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT autoclave_record_method_id_fkey FOREIGN KEY (method_id) REFERENCES method (id),
    CONSTRAINT autoclave_record_prepared_sample_id_fkey FOREIGN KEY (prepared_sample_id) REFERENCES prepared_sample (id),
    CONSTRAINT autoclave_record_raw_data_id_fkey FOREIGN KEY (raw_data_id) REFERENCES file_object_metadata (id),
    CONSTRAINT autoclave_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);
