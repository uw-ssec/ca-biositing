--
-- Name: observation; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS observation (
    record_id text NOT NULL,
    dataset_id integer,
    record_type text,
    parameter_id integer,
    value numeric,
    unit_id integer,
    dimension_type_id integer,
    dimension_value numeric,
    dimension_unit_id integer,
    note text,
    id SERIAL,
    created_at timestamp,
    updated_at timestamp,
    etl_run_id integer,
    lineage_group_id integer,
    CONSTRAINT observation_pkey PRIMARY KEY (id),
    CONSTRAINT observation_record_id_key UNIQUE (record_id),
    CONSTRAINT observation_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset (id),
    CONSTRAINT observation_dimension_type_id_fkey FOREIGN KEY (dimension_type_id) REFERENCES dimension_type (id),
    CONSTRAINT observation_dimension_unit_id_fkey FOREIGN KEY (dimension_unit_id) REFERENCES unit (id),
    CONSTRAINT observation_etl_run_id_fkey FOREIGN KEY (etl_run_id) REFERENCES etl_run (id),
    CONSTRAINT observation_parameter_id_fkey FOREIGN KEY (parameter_id) REFERENCES parameter (id),
    CONSTRAINT observation_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES unit (id)
);
