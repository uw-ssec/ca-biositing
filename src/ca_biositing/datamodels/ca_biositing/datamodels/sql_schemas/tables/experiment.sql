--
-- Name: experiment; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS experiment (
    analyst_id integer,
    exper_start_date date,
    exper_duration numeric,
    exper_duration_unit_id integer,
    exper_location_id integer,
    description text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT experiment_pkey PRIMARY KEY (id),
    CONSTRAINT experiment_analyst_id_fkey FOREIGN KEY (analyst_id) REFERENCES contact (id),
    CONSTRAINT experiment_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT experiment_exper_duration_unit_id_fkey FOREIGN KEY (exper_duration_unit_id) REFERENCES unit (id),
    CONSTRAINT experiment_exper_location_id_fkey FOREIGN KEY (exper_location_id) REFERENCES location_address (id)
);
