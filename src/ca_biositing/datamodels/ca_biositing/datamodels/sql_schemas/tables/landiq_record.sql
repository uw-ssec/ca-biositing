--
-- Name: landiq_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS landiq_record (
    record_id text NOT NULL,
    dataset_id integer,
    polygon_id integer,
    main_crop integer,
    secondary_crop integer,
    tertiary_crop integer,
    quaternary_crop integer,
    confidence integer,
    irrigated boolean,
    acres double precision,
    county text,
    version text,
    note text,
    pct1 double precision,
    pct2 double precision,
    pct3 double precision,
    pct4 double precision,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT landiq_record_pkey PRIMARY KEY (id),
    CONSTRAINT landiq_record_record_id_key UNIQUE (record_id),
    CONSTRAINT landiq_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT landiq_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT landiq_record_main_crop_fkey FOREIGN KEY (main_crop) REFERENCES primary_ag_product (id),
    CONSTRAINT landiq_record_polygon_id_fkey FOREIGN KEY (polygon_id) REFERENCES polygon (id),
    CONSTRAINT landiq_record_quaternary_crop_fkey FOREIGN KEY (quaternary_crop) REFERENCES primary_ag_product (id),
    CONSTRAINT landiq_record_secondary_crop_fkey FOREIGN KEY (secondary_crop) REFERENCES primary_ag_product (id),
    CONSTRAINT landiq_record_tertiary_crop_fkey FOREIGN KEY (tertiary_crop) REFERENCES primary_ag_product (id)
);
