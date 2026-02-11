--
-- Name: usda_market_report; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_market_report (
    slug_id integer,
    slug_name text,
    report_series_title text,
    frequency text,
    office_name text,
    office_city_id integer,
    office_state_fips text,
    source_id integer,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT usda_market_report_pkey PRIMARY KEY (id),
    CONSTRAINT usda_market_report_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT usda_market_report_office_city_id_fkey FOREIGN KEY (office_city_id) REFERENCES location_address (id),
    CONSTRAINT usda_market_report_source_id_fkey FOREIGN KEY (source_id) REFERENCES data_source (id)
);
