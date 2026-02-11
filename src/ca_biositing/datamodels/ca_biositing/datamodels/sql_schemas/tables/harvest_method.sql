--
-- Name: harvest_method; Type: TABLE; Schema: -; Owner: -
--

CREATE TABLE IF NOT EXISTS harvest_method (
    id SERIAL,
    name text,
    description text,
    uri text,
    CONSTRAINT harvest_method_pkey PRIMARY KEY (id)
);
