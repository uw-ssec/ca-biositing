--
-- Name: experiment_prepared_sample; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS experiment_prepared_sample (
    id SERIAL,
    experiment_id integer,
    prepared_sample_id integer,
    CONSTRAINT experiment_prepared_sample_pkey PRIMARY KEY (id),
    CONSTRAINT experiment_prepared_sample_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT experiment_prepared_sample_prepared_sample_id_fkey FOREIGN KEY (prepared_sample_id) REFERENCES prepared_sample (id)
);
