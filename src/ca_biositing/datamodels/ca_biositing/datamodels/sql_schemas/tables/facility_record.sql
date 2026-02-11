--
-- Name: facility_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS facility_record (
    dataset_id integer,
    facility_name text,
    location_id integer,
    capacity_mw numeric,
    resource_id integer,
    operator text,
    start_year integer,
    note text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT facility_record_pkey PRIMARY KEY (id),
    CONSTRAINT facility_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT facility_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT facility_record_location_id_fkey FOREIGN KEY (location_id) REFERENCES location_address (id),
    CONSTRAINT facility_record_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resource (id)
);
