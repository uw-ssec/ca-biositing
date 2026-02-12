--
-- Name: parameter_unit; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS parameter_unit (
    id SERIAL,
    parameter_id integer,
    alternate_unit_id integer,
    CONSTRAINT parameter_unit_pkey PRIMARY KEY (id),
    CONSTRAINT parameter_unit_alternate_unit_id_fkey FOREIGN KEY (alternate_unit_id) REFERENCES unit (id),
    CONSTRAINT parameter_unit_parameter_id_fkey FOREIGN KEY (parameter_id) REFERENCES parameter (id)
);
