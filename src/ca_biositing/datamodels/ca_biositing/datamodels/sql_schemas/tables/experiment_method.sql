--
-- Name: experiment_method; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS experiment_method (
    id SERIAL,
    experiment_id integer,
    method_id integer,
    CONSTRAINT experiment_method_pkey PRIMARY KEY (id),
    CONSTRAINT experiment_method_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id),
    CONSTRAINT experiment_method_method_id_fkey FOREIGN KEY (method_id) REFERENCES method (id)
);
