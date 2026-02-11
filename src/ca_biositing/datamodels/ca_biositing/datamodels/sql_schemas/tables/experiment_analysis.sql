--
-- Name: experiment_analysis; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS experiment_analysis (
    id SERIAL,
    experiment_id integer,
    analysis_type_id integer,
    CONSTRAINT experiment_analysis_pkey PRIMARY KEY (id),
    CONSTRAINT experiment_analysis_analysis_type_id_fkey FOREIGN KEY (analysis_type_id) REFERENCES analysis_type (id),
    CONSTRAINT experiment_analysis_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id)
);
