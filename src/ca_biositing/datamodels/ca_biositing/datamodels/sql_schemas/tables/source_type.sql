--
-- Name: source_type; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS source_type (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT source_type_pkey PRIMARY KEY (id)
);
