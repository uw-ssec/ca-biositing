--
-- Name: experiment_equipment; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS experiment_equipment (
    id SERIAL,
    experiment_id integer,
    equipment_id integer,
    CONSTRAINT experiment_equipment_pkey PRIMARY KEY (id),
    CONSTRAINT experiment_equipment_equipment_id_fkey FOREIGN KEY (equipment_id) REFERENCES equipment (id),
    CONSTRAINT experiment_equipment_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES experiment (id)
);
