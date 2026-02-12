--
-- Name: parameter_category_parameter; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS parameter_category_parameter (
    id SERIAL,
    parameter_id integer,
    parameter_category_id integer,
    CONSTRAINT parameter_category_parameter_pkey PRIMARY KEY (id),
    CONSTRAINT parameter_category_parameter_parameter_category_id_fkey FOREIGN KEY (parameter_category_id) REFERENCES parameter_category (id),
    CONSTRAINT parameter_category_parameter_parameter_id_fkey FOREIGN KEY (parameter_id) REFERENCES parameter (id)
);
