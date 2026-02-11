--
-- Name: usda_survey_record; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS usda_survey_record (
    dataset_id integer,
    geoid text,
    commodity_code integer,
    year integer,
    survey_program_id integer,
    survey_period text,
    reference_month text,
    seasonal_flag boolean,
    note text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT usda_survey_record_pkey PRIMARY KEY (id),
    CONSTRAINT usda_survey_record_commodity_code_fkey FOREIGN KEY (commodity_code) REFERENCES usda_commodity (id),
    CONSTRAINT usda_survey_record_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT usda_survey_record_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT usda_survey_record_survey_program_id_fkey FOREIGN KEY (survey_program_id) REFERENCES usda_survey_program (id)
);
