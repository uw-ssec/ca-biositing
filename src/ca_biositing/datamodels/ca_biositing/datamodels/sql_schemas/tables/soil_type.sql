--
-- Name: soil_type; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS soil_type (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT soil_type_pkey PRIMARY KEY (id)
);
