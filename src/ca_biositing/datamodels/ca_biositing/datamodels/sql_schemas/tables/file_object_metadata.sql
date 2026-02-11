--
-- Name: file_object_metadata; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS file_object_metadata (
    data_source_id integer,
    bucket_path text,
    file_format text,
    file_size integer,
    checksum_md5 text,
    checksum_sha256 text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT file_object_metadata_pkey PRIMARY KEY (id),
    CONSTRAINT file_object_metadata_data_source_id_fkey FOREIGN KEY (data_source_id) REFERENCES data_source (id),
    CONSTRAINT file_object_metadata_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id)
);
