--
-- Name: field_sample_condition; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS field_sample_condition (
    field_sample_id integer,
    ag_treatment_id integer,
    last_application_date date,
    treatment_amount_per_acre double precision,
    processing_method_id integer,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT field_sample_condition_pkey PRIMARY KEY (id),
    CONSTRAINT field_sample_condition_ag_treatment_id_fkey FOREIGN KEY (ag_treatment_id) REFERENCES ag_treatment (id),
    CONSTRAINT field_sample_condition_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT field_sample_condition_field_sample_id_fkey FOREIGN KEY (field_sample_id) REFERENCES field_sample (id),
    CONSTRAINT field_sample_condition_processing_method_id_fkey FOREIGN KEY (processing_method_id) REFERENCES processing_method (id)
);
