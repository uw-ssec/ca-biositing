--
-- Name: usda_market_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_market_record (
    report_id integer,
    dataset_id integer,
    report_begin_date timestamp,
    report_end_date timestamp,
    report_date timestamp,
    commodity_id integer,
    market_type_id integer,
    market_type_category text,
    grp text,
    market_category_id integer,
    class_ text,
    grade text,
    variety text,
    protein_pct numeric,
    application text,
    pkg text,
    sale_type text,
    price_unit_id integer,
    freight text,
    trans_mode text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT usda_market_record_pkey PRIMARY KEY (id),
    CONSTRAINT usda_market_record_commodity_id_fkey FOREIGN KEY (commodity_id) REFERENCES usda_commodity (id),
    CONSTRAINT usda_market_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT usda_market_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT usda_market_record_price_unit_id_fkey FOREIGN KEY (price_unit_id) REFERENCES unit (id),
    CONSTRAINT usda_market_record_report_id_fkey FOREIGN KEY (report_id) REFERENCES usda_market_report (id)
);
