--
-- Name: dimension_type; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS dimension_type (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT dimension_type_pkey PRIMARY KEY (id)
);
