--
-- Name: analysis_type; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS analysis_type (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT analysis_type_pkey PRIMARY KEY (id)
);
