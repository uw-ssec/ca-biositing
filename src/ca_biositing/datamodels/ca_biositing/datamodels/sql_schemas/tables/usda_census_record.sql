--
-- Name: usda_census_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_census_record (
    dataset_id integer,
    geoid text,
    commodity_code integer,
    year integer,
    source_reference text,
    note text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT usda_census_record_pkey PRIMARY KEY (id),
    CONSTRAINT usda_census_record_commodity_code_fkey FOREIGN KEY (commodity_code) REFERENCES usda_commodity (id),
    CONSTRAINT usda_census_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT usda_census_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id)
);
